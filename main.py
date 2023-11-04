import public.datebase as Datebase
import public.message as Message
import public.parser as Parser
import os
import importlib
import sys

PATH_MODULES = "./modules/"
headers = {}
s_headers = {}
modules = {}


def load_modules():
    sys.path.append(PATH_MODULES)
    mods = os.listdir(PATH_MODULES)
    mods = [i[:-3] for i in mods if i.endswith(".py")]
    for mod in mods:
        modules[mod] = __import__("kelpium")
        info = modules["kelpium"]._info()
        modules["kelpium"]._initialize()
        headers[mod] = info[0]
        s_headers[mod] = info[1]

    print(mods)


def distribute(msg, header, s_header, para, info):
    result = None
    if header:
        for h in headers.keys():
            if header in headers[h]:
                result = modules[h].exchange(msg, header, s_header, para, info)
    elif s_header:
        for h in s_headers.keys():
            if header in s_headers[h]:
                result = modules[h].exchange(msg, header, s_header, para, info)
    return result


if __name__ == '__main__':
    load_modules()
    print(headers)
    print(s_headers)

    while True:
        input_ = input("msg::")
        msg = Message.MessageChain()
        msg.append(Message.Text(input_))
        msg = msg.tostr()

        header = Parser.match_header(msg, "#")
        s_header = Parser.match_header(msg, "")
        para = Parser.parameter(msg)
        member = {"id": "114514", "name": "kelpman"}
        group = {"id": "1919810", "name": "kkbothome"}
        info = [member, group]
        result = distribute(msg, header=header, s_header=s_header, para=para, info=info)
        if result:
            print("result::", result.tostr())
        pass
