"""

    构建消息链

"""


class MessageChain(object):
    def __init__(self):
        super(MessageChain, self).__init__()
        self.lst = []

    def tostr(self):
        result = ""
        for element in self.lst:
            match element.type:
                case "Text":
                    result += element.text
                case "Image":
                    result += f" [Image:{element.url}]"
                case "At":
                    result += f" [At:{element.target}]"
        return result

    def append(self, element):
        self.lst.append(element)


class Text(object):
    def __init__(self, text: str):
        super(Text, self).__init__()
        self.type = "Text"
        self.text = text


class Image(object):
    def __init__(self, url: str):
        super(Image, self).__init__()
        self.type = "Image"
        self.url = url


class At(object):
    def __init__(self, target: str | int):
        super(At, self).__init__()
        self.type = "At"
        self.target = str(target)
