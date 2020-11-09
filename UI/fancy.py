import curses
import game
import time
import UI.colored_text
from UI.colored_text import ColorString
import logging
import os

LOG_DRAWING = False
REMOVED_BOTTOMLEFT = True

try: os.mkdir("logs")
except: pass
logging.basicConfig(level=logging.INFO if LOG_DRAWING else logging.WARNING, filename="logs/aaa.log")
keylog = logging.getLogger("keylogger")
keylog.addHandler(logging.FileHandler("logs/keylog.log"))
drawlog = logging.getLogger("drawlog")
drawlog.addHandler(logging.FileHandler("logs/drawlog.log"))


class FancyDrawer:
    def __init__(self):
        self.screen = None
        self.message_win = None
        global drawer
        drawer = self
        self.infection_text = "???"

    def __enter__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        self.screen.keypad(True)
        curses.curs_set(0)

        lines, columns = self.screen.getmaxyx()
        self.new_size(lines, columns)

        #self.message_win = curses.newwin(curses.LINES-1, curses.COLS-1, 0, 0)

        return self

    def __exit__(self, type, value, tb):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        self.screen = None
        curses.curs_set(1)
        return

    def __iter__(self):
        return self

    @staticmethod
    def write_text(window, text, noblanks=False):
        if LOG_DRAWING: drawlog.info(str(text))
        if isinstance(text, list):
            for element in text:
                FancyDrawer.write_text(window, element)
        elif isinstance(text, str):
            FancyDrawer.write_text(window, ColorString(text))
            #window.addstr(text)
            #drawlog.info(text)
        elif isinstance(text, UI.colored_text.ColorString):
            #drawlog.info("Colored: " + str(text))
            filter = game.game_state.glasses.type
            blanktext = "white" if noblanks else "blank"
            for chunk in text.glassed(game.game_state.get_stat("infection"), blanktext=blanktext):
                #drawlog.info("TEXT, COLOR: " + str(chunk))
                if not isinstance(chunk[1], int):
                    print(chunk)
                    time.sleep(5)
                curses.init_pair(chunk[1], chunk[1], -1)
                window.addstr(chunk[0], curses.color_pair(chunk[1]))
        else:
            raise TypeError("Whoopsie doopsie this must be a string or ColorString")

    def new_size(self, lines, columns):
        self.win_info =             curses.newwin(4, columns - 1, 0, 0)
        self.win_main =             curses.newwin((lines - 4) // 2, columns - 1, 4, 0)
        if not REMOVED_BOTTOMLEFT:
            self.win_idksemmozespisat = curses.newwin((lines - 4) // 2, (columns - 1) * 2 // 5, 4 + (lines - 4) // 2, 0)
            self.win_actionmenu = curses.newwin((lines - 4) // 2, (columns - 1) * 3 // 5, 4 + (lines - 4) // 2, (columns - 1) * 2 // 5)
        else:
            self.win_actionmenu = curses.newwin((lines - 4) // 2, (columns - 1), 4 + (lines - 4) // 2, 0)

    def draw(self, input_buffer):
        try:
            self.screen.move(0, 0)
            self.draw_info()
            self.draw_main()
            self.draw_actions(input_buffer)
            if not REMOVED_BOTTOMLEFT:
                self.draw_idkwindow()
            self.screen.refresh()
        except curses.error:
            print("Your terminal is too small. Recommended minimum size is 180x50")
            self.screen.refresh()

    def get_screen(self):
        return self.screen

    @staticmethod
    def make_bar(stat):
        return " "*round(game.game_state.get_stat(stat)*10) + "X"*round(10-(game.game_state.get_stat(stat)*10))

    def draw_info(self):
        lines, columns = self.screen.getmaxyx()
        lines, columns = 4, columns - 1
        self.win_info.move(0, 0)
        self.write_text(self.win_info, UI.colored_text.ColorString(("="*(columns-1), "red")))
        time = str(game.game_state.time)
        m = str(game.game_state.get_stat("money"))
        money = ColorString(("Money: [{0}]".format(" "*(4-len(m)) + m), "yellow"))
        energy = "Energy: 0[{0}]1".format(self.make_bar("energy"))
        willpower = ColorString(("Willpower: 0[{0}]1".format(self.make_bar("willpower")), "blue"))
        exhaustion = ColorString(("Hunger: 0[{0}]1".format(self.make_bar("hunger")), "magenta"))
        infection = ColorString((self.infection_text + ": 0[{0}]1".format(self.make_bar("infection")), "green"))
        weekday = ["Monday   ",
                   "Tuesday  ",
                   "Wednesday",
                   "Thursday ",
                   "Friday   ",
                   "Saturday ",
                   "Sunday   "][game.game_state.time.weekday()]
        tab = " "*(max((columns - len(time) - len(money) - len(energy) - len(willpower)) // 10, 1))

        for s in [tab*3, time, tab, money, tab*2, energy, tab, willpower, "\n"]:
            self.write_text(self.win_info, s, noblanks=True)

        for s in [tab*3, weekday, tab*3, " "*22, exhaustion, tab, " "*(9-len(self.infection_text)), infection, "\n"]:
            self.write_text(self.win_info, s, noblanks=True)

        self.write_text(self.win_info, UI.colored_text.ColorString(("="*(columns-1), "red")))

        self.win_info.clrtobot()
        self.win_info.refresh()

    def draw_main(self):
        lines, columns = self.screen.getmaxyx()
        self.win_main.move(0, 0)
        desc = game.game_state.location.description
        space = " "*((columns - 5 - len(desc)) // 2)
        self.write_text(self.win_main, "\n" + space + desc + space + "\n\n")
        if len(game.game_state.active_messages) > 0:
            drawlog.info("Active message: " + str(game.game_state.active_messages))
            for ind in range(len(game.game_state.active_messages)):
                self.write_text(self.win_main, ColorString(" ") + game.game_state.active_messages[ind] + "\n")
        self.win_main.clrtobot()
        self.win_main.refresh()

    def draw_actions(self, buffer):
        self.win_actionmenu.move(0, 0)
        lines, columns = self.screen.getmaxyx()
        if REMOVED_BOTTOMLEFT:
            lines, columns = (lines - 4) // 2, (columns - 1)
        else:
            lines, columns = (lines - 4) // 2, (columns - 1) * 3 // 5

        self.write_text(self.win_actionmenu, "=" * (columns) + "\n")

        self.write_text(self.win_actionmenu, "Action menu" + " "*(columns-12-len(buffer)))

        try:
            self.write_text(self.win_actionmenu, buffer + "\n")
        except:
            pass

        #self.win_actionmenu.addstr("="*20 + "\nAction menu")

        ind = 0
        for ac in game.game_state.visible_actions:
            if ind == game.game_state.highlighted_action:
                prefix = " -> "
            else:
                prefix = "   "
            txt = ColorString(prefix, str(ind+1), ": ") + ac.print() + "\n"
            self.write_text(self.win_actionmenu, txt)
            #self.write_text(self.win_actionmenu, "{0}{1}: {2}".format(prefix, ind + 1, ac.print()) + "\n")
            ind += 1


        self.win_actionmenu.clrtobot()
        self.win_actionmenu.refresh()

    def draw_idkwindow(self):
        self.win_idksemmozespisat.move(0, 0)
        lines, columns = self.screen.getmaxyx()
        lines, columns = (lines - 4) // 2, (columns - 1) * 2 // 5

        self.write_text(self.win_idksemmozespisat, "="*(columns))

        line = "|\n".join([" "*(columns-2) for i in range(lines-1)])
        self.write_text(self.win_idksemmozespisat, line)
        self.win_idksemmozespisat.clrtobot()
        self.win_idksemmozespisat.refresh()

    def classic_draw(self, buffer):
        raise NotImplemented
        state = game.game_state
        self.message_win.addstr("=" * 50 + "\n")
        self.message_win.addstr("Time: " + str(state.time)+ "\n")
        self.message_win.addstr(state.location.description+ "\n")
        if len(state.active_messages) > 0:
            self.message_win.addstr("--Messages"+ "\n")
            self.message_win.addstr("\n".join(state.active_messages)+ "\n")
        self.message_win.addstr("--Actions in " + state.location.name+ "\n")
        ind = 0
        for action in state.visible_actions:
            if action.enabled and action.visible:
                if ind == state.highlighted_action:
                    prefix = " -> "
                else:
                    prefix = "   "
                self.message_win.addstr("{0}{1}: {2}".format(prefix, ind + 1, action.print()) + "\n")
                ind += 1
        try:
            self.message_win.addstr(buffer + "\n")
        except:
            buffer = ""
        self.message_win.clrtobot()


class FancyInput:
    def __init__(self, screen, translator):
        self.screen = screen
        self.translator = translator
        self.delay = 0

    def __next__(self):
        return self.next()

    def __enter__(self):
        self.buffer = ""
        return self

    def __exit__(self, type, value, tb):
        return

    def __iter__(self):
        return self

    def next(self):
        time.sleep(self.delay)
        curses.flushinp()
        c = self.screen.getch()
        if LOG_DRAWING: keylog.info(str(c))
        if c == 27:
            self.delay = 0
            return "ESCAPE"
        elif chr(c).isdigit():
            self.delay = 0.1
            return chr(c)
        elif c == curses.KEY_BACKSPACE or c == ord("\b"):
            self.delay = 0
            if len(self.buffer) > 0:
                self.buffer = self.buffer[0:-1]
            return ""
        elif c == 10:
            self.delay = 0.1
            if len(self.buffer) > 0:
                temp = self.buffer
                self.buffer = ""
                return temp
            return 10
        elif c == curses.KEY_RESIZE:
            self.delay = 0
            drawer.new_size(*self.screen.getmaxyx())
        elif c in self.translator:
            self.delay = 0.08
            return c
        elif c < 256:
            self.delay = 0.01
            self.buffer += chr(c)
        return ""

drawer = FancyDrawer
generator = FancyInput