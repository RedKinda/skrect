import curses
import game
import time
import UI.colored_text
import logging

LOG_DRAWING = False


if LOG_DRAWING:
    import os
    try: os.mkdir("logs")
    except: pass
    logging.basicConfig(level=logging.INFO, filename="logs/aaa.log")
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
    def write_text(window, text):
        if LOG_DRAWING: drawlog.info(str(text))
        if isinstance(text, list):
            for element in text:
                FancyDrawer.write_text(window, element)
        elif isinstance(text, str):
            window.addstr(text)
            #drawlog.info(text)
        elif isinstance(text, UI.colored_text.ColorString):
            #drawlog.info("Colored: " + str(text))
            filter = game.game_state.glasses.type
            for chunk in text:
                #drawlog.info("TEXT, COLOR: " + str(chunk))
                curses.init_pair(1, chunk[1], -1)
                window.addstr(chunk[0], curses.color_pair(1))
        else:
            raise TypeError("Whoopsie doopsie this must be a string or ColorString")

    def new_size(self, lines, columns):
        self.win_info =             curses.newwin(4, columns - 1, 0, 0)
        self.win_main =             curses.newwin((lines - 4) // 2, columns - 1, 4, 0)
        self.win_idksemmozespisat = curses.newwin((lines - 4) // 2, (columns - 1) * 2 // 5, 4 + (lines - 4) // 2, 0)
        self.win_actionmenu =       curses.newwin((lines - 4) // 2, (columns - 1) * 3 // 5, 4 + (lines - 4) // 2, (columns - 1) * 2 // 5)

    def draw(self, input_buffer):
        try:
            self.screen.move(0, 0)
            self.draw_info()
            self.draw_main()
            self.draw_actions(input_buffer)
            self.draw_idkwindow()
            self.screen.refresh()
        except curses.error:
            print("Your terminal is too small. Recommended minimum size is 180x50")
            self.screen.refresh()

    def get_screen(self):
        return self.screen

    def draw_info(self):
        lines, columns = self.screen.getmaxyx()
        lines, columns = 4, columns - 1
        self.win_info.move(0, 0)
        self.write_text(self.win_info, UI.colored_text.ColorString(("="*(columns-1), "red")))
        time = str(game.game_state.time)
        money = "Money: [    ]"
        energy = "Energy: 0[          ]1"
        willpower = "Willpower: 0[          ]1"
        exhaustion = "Exhaustion: 1[          ]2"
        infection = "???: 0[          ]1"
        tab = " "*(max((columns - len(time) - len(money) - len(energy) - len(willpower)) // 10, 1))

        for s in [tab*3, time, tab, money, tab*2, energy, tab, willpower, "\n"]:
            self.write_text(self.win_info, s)

        for s in [tab*6, " "*27, exhaustion, tab, " "*6, infection, "\n"]:
            self.write_text(self.win_info, s)

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
            self.write_text(self.win_main, " " + "\n ".join(game.game_state.active_messages) + "\n")
        self.win_main.clrtobot()
        self.win_main.refresh()

    def draw_actions(self, buffer):
        self.win_actionmenu.move(0, 0)
        lines, columns = self.screen.getmaxyx()
        lines, columns = (lines - 4) // 2, (columns - 1) * 3 // 5

        self.write_text(self.win_actionmenu, "=" * (columns) + "\n")
        try:
            self.write_text(self.win_actionmenu, "Action menu" + " "*(columns-12-len(buffer)) + buffer + "\n")
        except:
            pass
        #self.win_actionmenu.addstr("="*20 + "\nAction menu")

        ind = 0
        for ac in game.game_state.visible_actions:
            if ind == game.game_state.highlighted_action:
                prefix = " -> "
            else:
                prefix = "   "
            self.write_text(self.win_actionmenu, "{0}{1}: {2}".format(prefix, ind + 1, ac.print()) + "\n")
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