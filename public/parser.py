'''
    消息链的参数解析器
'''


def match_header(message, tag="#"):
    if message[0:len(tag)] != tag:
        return False
    header = message.split(" ", 1)[0]
    return header


def parameter(message):
    paras = []  # 每个参数 [<type>,<para>] type为0为普通参数 type为1为特殊参数
    message = message.split(" ", 1)[1]
    flag = False

    name = ""
    para = ""
    for c in message:
        if c == ' ':
            if name and not flag:
                paras.append([0, name])
                name = ""
        elif c != '?':
            if not flag:
                name += c
            else:
                para += c
            # print(name, ':', para)
        elif c == '?':
            if flag:
                paras.append([1, {name: para}])
                flag = False
                name = ""
                para = ""
            elif not name:
                return "errors:para name not included"
            else:
                flag = True
    return paras
