#from curtsies.fmtfuncs import *

from game import Alignment


#Colored text is not implemented yet
raise NotImplemented

def blank(string):
    return black("*"*len(string))

def white(string):
    return string

translate_style = {
    "bold": bold,
    "underline": underline,
    "meta": underline,
    "keyword": bold
}

translate_color = {
    "red": red,
    "blue": blue,
    "green": green,
    "yellow": yellow,
    "magenta": magenta,
    "cyan": cyan,
    "white": white
}

translate_red_filter = {
    "red": red,
    "blue": blank,
    "green": blank,
    "yellow": red,
    "magenta": red,
    "cyan": blank,
    "white": red
}

translate_green_filter = {
    "red": blank,
    "blue": blank,
    "green": green,
    "yellow": green,
    "magenta": blank,
    "cyan": green,
    "white": green
}


class ColorString:
    def __init__(self, *args):
        self.text_chunks = []
        self.style_chunks = []
        for arg in args:
            if isinstance(arg, str):
                arg = (str, "white")
            self.text_chunks.append(arg[0])
            self.style_chunks.append(arg[1].split(" "))

    def __str__(self):
        return " ".join(self.text_chunks)

    def glassed(self, filter_color):
        result = ""
        for chunk_ind in range(len(self.text_chunks)):
            midresult = self.text_chunks[chunk_ind]
            for style in self.style_chunks[chunk_ind]:
                if style in translate_style:
                    midresult = translate_style[style](midresult)
                elif filter_color is Alignment.GOVERNMENT:
                    midresult = translate_red_filter[style](midresult)
                elif filter_color is Alignment.INDEPENDENT:
                    midresult = translate_color[style](midresult)
                elif filter_color is Alignment.HIVEMIND:
                    midresult = translate_green_filter[style](midresult)
            result += midresult
        return result



print(ColorString(("Thiss is a meta text and ", "meta"), ("this", "keyword"), (" is a keyword")).glassed(Alignment.GOVERNMENT))
