#from curtsies.fmtfuncs import *

from game import Alignment
import game
import curses
import random
import time


blank = "BLANK OWO"

translate_style = {
    "bold": curses.A_BOLD,
    "underline": curses.A_UNDERLINE,
    "meta": curses.A_UNDERLINE,
    "keyword": curses.A_BOLD,
    "blank": blank
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


def translate(text, style, translator):
    if style == "blank":
        color = blank
    else:
        color = translator[style]
    if color == blank:
        txt = " "*len(text)
        if len(text) > 0:
            if text[-1] == "\n":
                txt += "\n"
        return (txt, curses.COLOR_WHITE)
    else:
        return (text, color)

class ColorString:
    def __init__(self, *args):
        self.text_chunks = []
        self.style_chunks = []
        for arg in args:
            if isinstance(arg, str):
                arg = (arg, "white")
            self.text_chunks.append(str(arg[0]))
            self.style_chunks.append(arg[1])
        #print(self.text_chunks, self.style_chunks)

    def __str__(self):
        return "".join(self.text_chunks)

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

    def __add__(self, other):
        new = ColorString()
        for ch in self:
            new.text_chunks.append(ch[0])
            new.style_chunks.append(ch[1])
        if isinstance(other, ColorString):
            for ch in other:
                new.text_chunks.append(ch[0])
                new.style_chunks.append(ch[1])
        elif isinstance(other, str):
            new.text_chunks.append(other)
            new.style_chunks.append("white")
        else:
            raise TypeError("operator '+' can only be used on strings and ColorStrings")
        return new

    def __len__(self):
        return len("".join(self.text_chunks))

    def lower(self):
        return str(self).lower()

    def glassed(self, infection, filter=None, blanktext="blank"):
        if filter is None:
            filter = game.game_state.glasses.type if game.game_state else Alignment.INDEPENDENT
        if filter == Alignment.GOVERNMENT:
            translator = translate_red_filter
        elif filter == Alignment.INDEPENDENT:
            translator = translate_color
        elif filter == Alignment.HIVEMIND:
            translator = translate_green_filter
        else:
            raise TypeError("Invalid filter type")

        new = ColorString()
        for i in range(len(self.text_chunks)):
            text, style = self.text_chunks[i], self.style_chunks[i]
            words = text.split(" ")
            styles = [style for k in range(len(words))]
            for j in range(len(words)):
                if len(words[j]) > 2:
                    if words[j][0:3] == "Red":
                        styles[j] = 'red'
                if j != len(words) - 1:
                    words[j] += " "
                if random.random() <= infection:
                    if game.game_state.glasses.type == game.Alignment.GOVERNMENT:
                        tup = translate(words[j], blanktext, translate_red_filter)
                    else:
                        tup = translate(words[j], styles[j], translate_green_filter)
                else:
                    tup = translate(words[j], styles[j], translator)
                new.text_chunks.append(tup[0])
                new.style_chunks.append(tup[1])
        return new

'''    def glassed(self, filter_color):
        newchunks = []
        for chunk_ind in range(len(self.text_chunks)):
            midstyle = None
            if self.style_chunks[chunk_ind] in translate_style:
                midstyle = translate_style[self.style_chunks[chunk_ind]]
            elif filter_color is Alignment.GOVERNMENT:
                midstyle = translate_red_filter[self.style_chunks[chunk_ind]]
            elif filter_color is Alignment.INDEPENDENT:
                midstyle = translate_color[self.style_chunks[chunk_ind]]
            elif filter_color is Alignment.HIVEMIND:
                midstyle = translate_green_filter[self.style_chunks[chunk_ind]]
            newchunks.append(midstyle)

        result = ColorString()
        result.text_chunks = [c for c in self.text_chunks]
        result.style_chunks = [s for s in newchunks]
        return result'''


#a = ColorString(" ") + ColorString(("Something brrr", "red")) + "\n"
#print(str(a))
#print(ColorString(("Thiss is a meta text and ", "meta"), ("this", "keyword"), (" is a keyword")).glassed(Alignment.GOVERNMENT))
