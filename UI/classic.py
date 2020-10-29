import game
import curses


class ClassicDrawer:
    def draw(self, *args):
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
        self.buffer = ""
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
            "": curses.KEY_ENTER,
        }
        char = input()
        if char in translation:
            return translation[char]
        return str(char)

