"""
kelpium货币系统
headers:
    #kp #kelpium
    #give
    #pk
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
import random


# 必备的bot规范
def _info():
    headers = ["#kp", "#kelpium", "#give", "#pk", "#beg", "#signin", "#sign_in"]
    s_headers = ["donate", "accept", "reject", "shot"]  # s_headers = None  捕捉特殊消息
    return [headers, s_headers]


# 初始化
def _initialize():
    Datebase.initialize("kelpium.db")
    table = ["KELPIUM(ID INT, KELPIUM INT default 0)",
             "DAILY_KELPIUM(ID INT, KELPIUM INT default 0,DATETIME TEXT)"]
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
                pass
            case "#beg":
                pass
    elif s_header:
        match s_header:
            case "donate":
                pass
            case "accept":
                pass
            case "reject":
                pass
            case "shot":
                pass


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
        Datebase.insert(name_db=name_db, table=table, key=key, values=values)

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
        Datebase.insert(name_db=name_db, table=table, key=key, values=values)
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
        for i in range(0, len(ranking)):
            if ranking[i][1] <= kelpium:
                break
        else:
            i += 1
        ranking.insert(i, [m.name, kelpium])

    result = "=====KELPIUM-RANKING=====\n KELPIUM   NAME"
    for r in ranking:
        kelpium_len = len(str(r[1]))
        result += " " * (9 - kelpium_len) + str(r[1]) + "  " + r[0] + "\n"
    result += "========================="
    return result
