import curses
import traceback

import game


class FancyDrawer:
    def __init__(self):
        self.screen = None
        self.message_win = None

    def __enter__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.screen.keypad(True)
        curses.curs_set(0)

        lines, columns = self.screen.getmaxyx()
        self.new_size(lines, columns)

        self.message_win = curses.newwin(curses.LINES-1, curses.COLS-1, 0, 0)

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

    def new_size(self, lines, columns):
        self.win_info = curses.newwin(4, columns - 1, 0, 0)
        self.win_main = curses.newwin((lines - 4) // 2, columns - 1, 4, 0)
        self.win_idksemmozespisat = curses.newwin((lines - 4) // 2, (columns - 1) * 2 // 5,
                                                  4 + (lines - 4) // 2, 0)
        self.win_actionmenu = curses.newwin((lines - 4) // 2, (columns - 1) * 3 // 5,
                                            4 + (lines - 4) // 2, (columns - 1) * 2 // 5)

    def draw(self):
        #for message in game.game_state.active_messages:
        #    self.message_win.addstr(message + "\n")
        self.classic_draw()
        self.message_win.move(0, 0)
        self.screen.refresh()
        self.message_win.refresh()

    def get_screen(self):
        return self.screen

    def draw_info(self):
        self.win_info.move(0, 0)
        #self.win_info.addstr("="*self.win_info.)

    def classic_draw(self):
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
                    prefix = "-> "
                else:
                    prefix = "   "
                self.message_win.addstr("{0}{1}: {2}".format(prefix, ind + 1, action.print()) + "\n")
                ind += 1
        self.message_win.addstr(input_generator.buffer + "\n")
        self.message_win.clrtobot()



class FancyInput:
    def __init__(self, screen):
        self.screen = screen

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
        c = self.screen.getch()
        if c == 27:
            return "ESCAPE"
        elif chr(c).isdigit():
            return chr(c)
        elif c == curses.KEY_BACKSPACE:
            if len(self.buffer) > 0:
                self.buffer = self.buffer[0:-1]
            return ""
        elif c == 10:
            if len(self.buffer) > 0:
                temp = self.buffer
                self.buffer = ""
                return temp
            return 10
        elif c in translator:
            return c
        elif c < 256:
            self.buffer += chr(c)
        return ""


class ClassicDrawer:
    def draw(self):
        state = game.game_state
        print("="*50)
        print("Time: " + str(state.time))
        print(state.location.description)
        if len(state.active_messages) > 0:
            print("--Messages")
            print("\n".join(state.active_messages))
        print("--Actions in " + state.location.name)
        ind = 0
        for action in state.visible_actions:
            if action.enabled and action.visible:
                if ind == state.highlighted_action:
                    prefix = "-> "
                else:
                    prefix = "   "
                print("{0}{1}: {2}".format(prefix, ind+1, action.print()))
                ind += 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        return

    def __iter__(self):
        return self

    def get_screen(self):
        return "no screen"


class ClassicInput:
    def __init__(self, *args):
        pass

    def __next__(self):
        return self.next()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        return

    def __iter__(self):
        return self

    def next(self):
        translation = {
            "w": curses.KEY_UP,
            "a": curses.KEY_LEFT,
            "s": curses.KEY_DOWN,
            "d": curses.KEY_RIGHT,
            "": curses.KEY_ENTER
        }
        char = input()
        if char in translation:
            return translation[char]
        return str(char)


try:  # Fancy curtsies drawer
    with FancyDrawer() as d:
        pass
    generator = FancyInput
    drawer = FancyDrawer
except:  # Fallback to simple drawing for dumb terminals
    print("You can safely ignore the following error:")
    traceback.print_exc()
    print("Warning! Using the uglier version of interface, use smart terminal for the nice version")
    generator = ClassicInput
    drawer = ClassicDrawer


from redacted import shop
shop.run()


translator = {
    curses.KEY_UP: game.game_state.input_up,
    curses.KEY_DOWN: game.game_state.input_down,
    10: game.game_state.input_enter
}

with drawer() as drawer:
    with generator(drawer.get_screen()) as input_generator:
        #print("Starting game cycle...")
        drawer.draw()
        for inp in input_generator:
            if inp == "ESCAPE":
                break
            elif inp in translator:
                translator[inp]()
            elif len(inp) > 1:
                game.game_state.execute_action_by_string(inp)
            elif inp.isdigit():
                game.game_state.execute_action_from_list(int(inp)-1)
            drawer.draw()







'''print(yellow('this prints normally, not to the alternate screen'))
with FullscreenWindow() as window:
    with generator() as input_generator:
        msg = red(on_blue(bold('Press escape to exit')))
        a = FSArray(window.height, window.width)
        a[0:1, 0:msg.width] = [msg]
        window.render_to_terminal(a)
        for c in input_generator:
            if c == '<ESC>':
                break
            elif c == '<SPACE>':
                a = FSArray(window.height, window.width)
            else:
                s = repr(c)
                row = random.choice(range(window.height))
                column = random.choice(range(window.width-len(s)))
                color = random.choice([red, green, on_blue, yellow])
                a[row, column:column+len(s)] = [color(s)]
            window.render_to_terminal(a)'''
