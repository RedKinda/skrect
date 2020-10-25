import game
import re

class FancyDrawer:
    def __init__(self):
        raise NotImplemented

    def color_text(self, text):
        re_red = re.compile("<red>(?P<red>.*)</red>")
        re_blue = re.compile("<blue>(?P<blue>.*)</blue>")
        re_white = re.compile("<white>(?P<white>.*)</white>")
        re_green = re.compile("<green>(?P<green>.*)</green>")




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


class ClassicInput:
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
            "w": "<UP>",
            "a": "<LEFT>",
            "s": "<DOWN>",
            "d": "<RIGHT>",
            "": "<Ctrl-j>"
        }
        char = input()
        if char in translation:
            return translation[char]
        return char


try:  # Fancy curtsies drawer
    import curtsies
    from curtsies import FullscreenWindow, Input, FSArray
    from curtsies.fmtfuncs import red, bold, green, on_blue, yellow
    with Input() as gen:
        pass
    generator = Input
    drawer = FancyDrawer
except:  # Fallback to simple drawing for dumb terminals
    print("Warning! Using the uglier version of interface, use smart terminal for the nice version")
    generator = ClassicInput
    drawer = ClassicDrawer


from sample_world import sample1
sample1.run()


translator = {
    "<UP>": game.game_state.input_up,
    "<DOWN>": game.game_state.input_down,
    "<Ctrl-j>": game.game_state.input_enter
}

with drawer() as drawer:
    with generator() as input_generator:
        print("Starting game cycle...")
        drawer.draw()
        for inp in input_generator:
            if inp == "<ESC>":
                break
            elif inp in translator:
                translator[inp]()
            elif len(inp) > 1:
                game.game_state.execute_action_by_string(inp)
            elif inp.isdigit():
                game.game_state.execute_action(int(inp)-1)
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

