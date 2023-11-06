"""
wordle
headers:
    #wd [n默认为5]
    #wd stop
s_headers:
    ?*****
"""

import public.datebase as Datebase
import public.message as Msg
import datetime
import random


# 必备的bot规范
def _info():
    headers = ["#wd"]
    s_headers = ["?"]  # s_headers = None  捕捉特殊消息
    return [headers, s_headers]


# 初始化
def _initialize():
    pass
    # Datebase.initialize("wordle.db")
    # table = ["?(ID INT, KELPIUM INT default 0)","]
    # Datebase.create_table("kelpium.db", table)


# 交换msg
def exchange(msg, header=None, s_header=None, para=None, info=None):  # info[0]:member info[1]:group
    if para:
        pass
    if header:
        match header:
            case "#wd":
                return wd(msg, para, info)
    elif s_header:
        match s_header:
            case "?":
                pass


#  #kp  #kelpium
def wd(msg, para, info):
    result = None

    wordle_length = 5
    match len(para):
        case 0:
            pass
        case 1:
            if para[0][0] == 0 and para[0][1]:  # 指定长度wordle
                length = para[0][1]
                if not length.isdigit() or not (2 <= int(para[0][1]) <= 22):  # 非法长度
                    result = Msg.MessageChain()
                    result.append(Msg.Text("长度非法，请检查"))
                else:  # 长度非法
                    wordle_length = int(length)

    return result
