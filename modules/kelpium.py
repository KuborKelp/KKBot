"""
kelpium货币系统
headers:
    #kp #kelpium
    #give
    #beg
s_headers:
    donate
    accept
    reject
    shot
"""

import public.datebase as Datebase
import public.message as Msg
import datetime
import time
import random

PROBABILTY = [25, 36, 69, 88, 99, 100]


# 必备的bot规范
def _info():
    headers = ["#kp", "#kelpium", "#give", "#pk", "#beg", "#signin", "#sign_in"]
    s_headers = ["donate", "accept", "shot"]  # s_headers = None  捕捉特殊消息
    return [headers, s_headers]


# 初始化
def _initialize():
    Datebase.initialize("kelpium.db")
    table = ["KELPIUM(ID INT, KELPIUM INT default 0)",
             "DAILY_KELPIUM(ID INT, KELPIUM INT default 0,DATETIME TEXT)",
             "PK_QUEUE(GID INT, KELPIUM INT,HOST INT ,TIME INT)",  # pk匹配队列: 群号 金额 房主 时间
             "PK_LIST(GID INT, KELPIUM INT,HOST INT, PLAYER INT,TIME INT,ROUND INT)"
             # pk游戏队列: 群号 金额 房主 玩家 时间 回合
             ]
    Datebase.create_table("kelpium.db", table)


# 交换msg
def exchange(msg, header=None, s_header=None, para=None, info=None):  # info[0]:member info[1]:group
    if para:
        pass
    if header:
        match header:
            case "#kp" | "#kelpium":
                return kelpium(msg, para, info)
            case "#signin" | "#sign_in":
                return signin(msg, para, info)
            case "#give":
                pass
            case "#pk":
                return pk(msg, para, info)
            case "#beg":
                pass
    elif s_header:
        match s_header:
            case "donate":
                pass
            case "accept":
                if msg == "accept":
                    return accept_pk(msg, para, info)
            case "shot":
                if msg == "shot":
                    return shot(msg, para, info)


#  #kp  #kelpium
def kelpium(msg, para, info):
    result = None
    match len(para):
        case 0:
            kelpium = select_kelpium(info[0])  # info[0]:member_info
            result = Msg.MessageChain()
            result.append(Msg.Text(f"{info[0]['name']} 拥有 {kelpium}kelpium"))
        case 1:
            if para[0][0] == 0 and para[0][1] == "ranking":
                ranking = get_kelpium_ranking(info[1])
                result = Msg.MessageChain()
                result.append(Msg.Text(ranking))
    return result


def signin(msg, para, info):
    today_kelpium, kelpium = daily_kelpium(info[0])
    result = Msg.MessageChain()
    result.append(Msg.Text(f"{info[0]['name']} 今天获得了{today_kelpium}kelpium"))
    return result


def pk(msg, para, info):
    result = Msg.MessageChain()
    gid = info[1]["id"]
    host_id = info[0]["id"]
    kelpium = 10
    if para:
        if para[0][0] == 0:
            if not para[0][1].isdigit():
                result.append(Msg.Text(f"非法数据: {kelpium}"))
                return result
            kelpium = int(para[0][1])
            if kelpium <= 0:
                result.append(Msg.Text(f"非法数据: {kelpium}"))
                return result
    # 获取 pk匹配队列和pk游戏列表
    pk_queue = select_pk_queue(gid)
    pk_list = select_pk_list(gid)
    print("queue:", pk_queue)
    print("list:", pk_list)

    if pk_queue or pk_list:  # 检测是否 占用队列/游戏
        if pk_queue == [0] or pk_list == [0]:
            result.append(Msg.Text(f"上一场对局超时120s!已强制结束!"))
        elif pk_queue[0] == 1:
            queue_host = pk_queue[1][0][2]
            result.append(Msg.Text(f"{queue_host}的pk正在匹配中!"))
            return result
        elif pk_list[0] == 1:
            list_host = pk_list[1][0][2]
            result.append(Msg.Text(f"{list_host}发起的pk正在进行中!"))
            return result
    else:  # 发起对局
        host_kelpium = select_kelpium(info[0])  # 获取房主KELPIUM数额
        if host_kelpium < kelpium:
            result.append(Msg.Text(f"{host_id}Kelpium不足!"))
            return result

        time = get_time()
        name_db = "kelpium.db"
        table = "PK_QUEUE"
        key = "(GID,KELPIUM,HOST,TIME)"
        values = f"({gid},{kelpium},{host_id},{time})"

        Datebase.insert(name_db=name_db, table=table, key=key, value=values)
        result.append(Msg.Text(f"已发起赌注为{kelpium}的对局,请输入accept接受对局,否则将在120s后失效"))
    return result


def accept_pk(msg, para, info):
    result = Msg.MessageChain()
    gid = info[1]["id"]
    player_id = info[0]["id"]

    pk_queue = select_pk_queue(gid)
    pk_list = select_pk_list(gid)

    if pk_queue or pk_list:  # 检测是否 占用队列/游戏
        if pk_queue == [0] or pk_list == [0]:
            result.append(Msg.Text(f"上一场对局超时120s!已强制结束!"))
        elif pk_list and pk_list[0] == 1:
            list_host = pk_list[1][0][2]
            result.append(Msg.Text(f"{list_host}发起的pk正在进行中!"))
            return result
        else:  # 发起对局前检测
            if pk_queue[0] == 1:
                host_id = pk_queue[1][0][2]
                kelpium = pk_queue[1][0][1]
                host_kelpium = select_kelpium({"id": host_id})  # 获取房主KELPIUM数额
                player_kelpium = select_kelpium(info[0])  # 获取玩家KELPIUM数额
                if str(host_id) == str(player_id):
                    result.append(Msg.Text("请勿自娱自乐:)"))
                    return result
                elif host_kelpium < kelpium or player_kelpium < kelpium:
                    result.append(Msg.Text(f"有人Kelpium不足我不说是谁,这局需要{kelpium}kelpium哦!"))
                    return result
                else:  # 开始对局
                    first = random.randint(0, 1)
                    if first:  # 随机一下初始玩家
                        host_id, player_id = player_id, host_id

                    name_db = "kelpium.db"
                    table = "PK_QUEUE"
                    Datebase.delete(name_db=name_db, table=table, key="GID", value=gid)

                    table = "PK_LIST"
                    key = "(GID,KELPIUM,HOST,PLAYER,TIME,ROUND)"
                    values = f"({gid},{kelpium},{host_id},{player_id},{get_time()},{0})"
                    Datebase.insert(name_db=name_db, table=table, key=key, value=values)
                    result.append(Msg.Text(f"现在轮到{player_id}开枪,请您发送: shot ,GG概率为{PROBABILTY[0]}%"))
                    return result


def shot(msg, para, info):
    result = Msg.MessageChain()
    gid = info[1]["id"]
    pk_list = select_pk_list(gid)

    if pk_list:
        if pk_list == [0]:
            result.append(Msg.Text(f"上一场对局超时120s!已强制结束!"))
            return result
        elif pk_list and pk_list[0] == 1:

            player_id = str(info[0]["id"])
            host = str(pk_list[1][0][2])

            kelpium = pk_list[1][0][1]  # 赌金
            host_id = pk_list[1][0][2]  # 当前开枪者
            player_id = pk_list[1][0][3]  # 另一个玩家
            round = pk_list[1][0][5]

            if player_id == str(host_id):
                # 先删除对局,如果游戏没结束再添加回去
                name_db = "kelpium.db"
                table = "PK_QUEUE"
                Datebase.delete(name_db=name_db, table=table, key="GID", value=gid)
                # 开枪
                if random.randint(0, 100) < PROBABILTY[round]:
                    # 结束对局
                    result.append(f"{host_id}输了!")
                    return result
                else:
                    table = "PK_LIST"
                    key = "(GID,KELPIUM,HOST,PLAYER,TIME,ROUND)"
                    host_id, player_id = player_id, host_id  # 交换开枪顺序
                    values = f"({gid},{kelpium},{host_id},{player_id},{get_time()},{round + 1})"
                    Datebase.insert(name_db=name_db, table=table, key=key, value=values)
                    result.append(f"GG概率为{PROBABILTY[0]}%")
                    return result


def daily_kelpium(member_info):
    member_id = member_info["id"]
    kelpium = select_kelpium(member_info)  # info[0]:member_info

    time = get_time_today()
    name_db = "kelpium.db"
    table = "DAILY_KELPIUM"
    key = {'ID': str(member_id), 'DATETIME': time}

    result = Datebase.select(name_db=name_db, table=table, key=key)
    if not result:
        daily_kelpium = random.randint(1, 100)
        key = "(ID,KELPIUM,DATETIME)"
        values = f"({member_id},{daily_kelpium},{time})"
        Datebase.insert(name_db=name_db, table=table, key=key, value=values)

        kelpium += daily_kelpium
        table = "KELPIUM"
        key = ['ID', member_id]
        values = ["KELPIUM", kelpium]
        Datebase.update(name_db=name_db, table=table, key=key, values=values)
    else:
        daily_kelpium = result[0][1]
    return daily_kelpium, kelpium


def get_time_today():
    return str(datetime.date.today()).replace('-', '')


def get_time():
    return int(time.time())


def select_kelpium(member_info):
    member_id = member_info["id"]
    # member_name = member_info["name"]

    name_db = "kelpium.db"
    table = "KELPIUM"
    key = {"ID": member_id}
    result = Datebase.select(name_db=name_db, table=table, key=key)
    if not result:
        key = "(ID,KELPIUM)"
        values = f"({member_id},{0})"
        Datebase.insert(name_db=name_db, table=table, key=key, value=values)
        result = 0
    else:
        result = result[0][1]
    return result


def get_kelpium_ranking(group_info):
    # group_id = group_info["id"]
    member_list = group_info["members"]
    name_db = "kelpium.db"
    table = "KELPIUM"

    ranking = []

    for m in member_list:
        member_info = {"id": m.id}
        kelpium = select_kelpium(member_info)
        i = 0
        if not kelpium:
            continue
        for i in range(0, len(ranking)):
            if ranking[i][1] <= kelpium:
                break
        else:
            i += 1
        ranking.insert(i, [m.name, kelpium])

    ranking = ranking[:15]
    result = "=====KELPIUM-RANKING=====\n KELPIUM   NAME\n"
    for r in ranking:
        kelpium_len = len(str(r[1]))
        result += str(r[1]) + " " * (12 - kelpium_len) + "  " + r[0] + "\n"
    result += "========================="
    return result


def select_pk_queue(gid):
    name_db = "kelpium.db"
    table = "PK_QUEUE"
    key = {"GID": gid}
    result = Datebase.select(name_db=name_db, table=table, key=key)
    if result:
        time = get_time()
        if time - result[0][3] > 120:  # 超时检测
            Datebase.delete(name_db=name_db, table=table, key="GID", value=gid)
            return [0]
        else:
            return [1, result]
    return None


def select_pk_list(gid):
    name_db = "kelpium.db"
    table = "PK_LIST"
    key = {"GID": gid}
    result = Datebase.select(name_db=name_db, table=table, key=key)
    if result:
        time = get_time()
        if time - result[0][3] > 120:  # 超时检测
            Datebase.delete(name_db=name_db, table=table, key="GID", value=gid)
            return [0]
        else:
            return [1, result]
    return None
