import public.datebase as datebase
import public.message as message
import public.parser as parser
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
        headers[mod] = info[0]
        s_headers[mod] = info[1]

    print(mods)


if __name__ == '__main__':
    load_modules()
    print(headers)
    print(s_headers)
    pass
