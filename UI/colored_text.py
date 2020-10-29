#from curtsies.fmtfuncs import *

from game import Alignment
import curses

#Colored text is not implemented yet
blank = None

translate_style = {
    "bold": curses.A_BOLD,
    "underline": curses.A_UNDERLINE,
    "meta": curses.A_UNDERLINE,
    "keyword": curses.A_BOLD
}

translate_color = {
    "red": curses.COLOR_RED,
    "blue": curses.COLOR_BLUE,
    "green": curses.COLOR_GREEN,
    "yellow": curses.COLOR_YELLOW,
    "magenta": curses.COLOR_MAGENTA,
    "cyan": curses.COLOR_CYAN,
    "white": curses.COLOR_WHITE
}

translate_red_filter = {
    "red": curses.COLOR_RED,
    "blue": blank,
    "green": blank,
    "yellow": curses.COLOR_RED,
    "magenta": curses.COLOR_RED,
    "cyan": blank,
    "white": curses.COLOR_RED
}

translate_green_filter = {
    "red": blank,
    "blue": blank,
    "green": curses.COLOR_GREEN,
    "yellow": curses.COLOR_GREEN,
    "magenta": blank,
    "cyan": curses.COLOR_GREEN,
    "white": curses.COLOR_GREEN
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

    def __iter__(self):
        self.ind = 0
        return self

    def __next__(self):
        if self.ind < len(self.text_chunks):
            tup = (self.text_chunks[self.ind], self.style_chunks[self.ind])
            self.ind += 1
            return tup
        else:
            raise StopIteration

    def glassed(self, filter_color):
        newchunks = []
        for chunk_ind in range(len(self.text_chunks)):
            midstyle = None
            for style in self.style_chunks[chunk_ind]:
                if style in translate_style:
                    midstyle |= translate_style[style]
                elif filter_color is Alignment.GOVERNMENT:
                    midstyle |= translate_red_filter[style]
                elif filter_color is Alignment.INDEPENDENT:
                    midstyle |= translate_color[style]
                elif filter_color is Alignment.HIVEMIND:
                    midstyle |= translate_green_filter[style]

        result = ColorString()
        result.text_chunks = [c for c in self.text_chunks]
        result.style_chunks = [s for s in newchunks]
        return result



print(ColorString(("Thiss is a meta text and ", "meta"), ("this", "keyword"), (" is a keyword")).glassed(Alignment.GOVERNMENT))
