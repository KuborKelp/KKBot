'''
kelpium 货币系统
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
'''


# 必备的bot规范
def _info():
    headers = ["#kp", "#kelpium", "#give", "#pk", "#beg"]
    s_headers = ["donate", "accept", "reject", "shot"]  # s_headers = None  捕捉特殊消息
    return [headers, s_headers]


# 初始化
def _initialize():
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
    return [["Text", "hELLO wORLD"]]


def te():
    return "11121"
