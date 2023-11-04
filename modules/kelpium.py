'''
kelpium 货币系统
headers:
    #kp #kelpium
    #signin #sign_in
    #give
    #pk
    #beg
s_headers:
    donate
    accept
    reject
    shot
'''

import public.datebase as Datebase
import public.message as Msg


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
    pass


# 交换msg
def exchange(msg, header=None, s_header=None, para=None, info=None):  # info[0]:member info[1]:group
    if para:
        pass
    if header:
        match header:
            case "#kp" | "kelpium":
                return kelpium(msg, para, info)
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
    kelpium = select_kelpium(info[0])  # info[0]:member_info
    result = Msg.MessageChain()
    result.append(Msg.Text(f"{info[0]['id']} has {kelpium}kelpium"))
    return result


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
