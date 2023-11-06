from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, At, Quote
from graia.ariadne.model import Group, Member
from graia.broadcast import Broadcast
import sys
import os

import public.datebase as Datebase
import public.message as Message
import public.parser as Parser

PATH_MODULES = "./modules/"
headers = {}
s_headers = {}
modules = {}

# with open('config.txt', 'r') as cf:
#     qq = int(cf.readline().replace('\n', ''))
qq = 3553949758

def load_modules():
    sys.path.append(PATH_MODULES)
    mods = os.listdir(PATH_MODULES)
    mods = [i[:-3] for i in mods if i.endswith(".py")]
    for mod in mods:
        modules[mod] = __import__(mod)
        info = modules[mod]._info()
        modules[mod]._initialize()
        headers[mod] = info[0]
        s_headers[mod] = info[1]


load_modules()
bcc = create(Broadcast)
app = Ariadne(
    connection=config(
        qq,  # 你的机器人的 qq 号
        "ServiceVerifyKey",  # 填入你的 mirai-api-http 配置中的 verifyKey
        # 以下两行代码（不含注释）里的 host 参数的地址
        # 是你的 mirai-api-http 地址中的地址与端口
        # 他们默认为 "http://localhost:8080"
        # 如果你 mirai-api-http 的地址与端口也是 localhost:8080
        # 就可以删掉这两行，否则需要修改为 mirai-api-http 的地址与端口
    ),
)


@bcc.receiver(GroupMessage)
async def group_message_listener(app: Ariadne, group: Group, message: MessageChain, member: Member,
                                 quote: Quote | None):
    # msg = message.display
    msg = destruction(message)
    result = None
    header = Parser.match_header(msg, "#")
    s_header = Parser.match_header(msg, "")
    para = Parser.parameter(msg)

    new_member = {"id": member.id, "name": member.name}
    members_list = await app.get_member_list(group)
    new_group = {"id": group.id, "name": group.name, "members": members_list}
    info = [new_member, new_group]
    result = distribute(msg, header=header, s_header=s_header, para=para, info=info)
    if result:
        msgchain = construct(result)
        await app.send_message(group, msgchain)


def distribute(msg, header, s_header, para, info):
    result = None
    if header:
        for h in headers.keys():
            if header in headers[h]:
                result = modules[h].exchange(msg, header, s_header, para, info)
    elif s_header:
        for h in s_headers.keys():
            if s_header in s_headers[h]:
                result = modules[h].exchange(msg, header, s_header, para, info)
    return result


def destruction(message):
    msg = ""
    for element in message:
        if element.type == "Image":
            msg += f" [Image:{element.url}] "
        elif element.type == "Plain":
            msg += f"{element.text}"
        elif element.type == "At":
            msg += f" [Image:{element.target}] "
    return msg


def construct(msg):
    msgchain = MessageChain([])
    for element in msg.lst:
        match element.type:
            case "Text":
                msgchain.append(Plain(text=element.text))
            case "Image":
                msgchain.append(Image(path=element.url))
            case "At":
                msgchain.append(At(target=element.target))

    return msgchain


app.launch_blocking()
