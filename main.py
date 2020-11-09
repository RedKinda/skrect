import curses
import traceback
import time
import game
import UI.sound

DEBUG = False
#from sample_world.sample1 import run
#from redacted.shop import run
from redacted.streets.mainroad import run
run()


translator = {
    curses.KEY_UP: game.game_state.input_up,
    curses.KEY_DOWN: game.game_state.input_down,
    curses.KEY_ENTER: game.game_state.input_enter,
    10: game.game_state.input_enter
}


try:  # Fancy curtsies drawer
    print("Trying on fancy pants...")
    from UI.fancy import drawer, generator
    with drawer() as dr:
        with generator(dr.get_screen(), {}) as gen:
            dr.draw(gen.buffer)
    UI.sound.play_forever()
    print("Pants work! Starting fancy terminal...")
    print("You can exit the game any time by pressing the escape button")
    input("Once you press ENTER don't forget to maximize your terminal for the best experience!")
except:  # Fallback to simple drawing for dumb terminals
    from UI.classic import ClassicDrawer, ClassicInput

    UI.sound.play_forever()
    if DEBUG:
        print("You can safely ignore the following error:")
        traceback.print_exc()
    print("Warning! Using the 'classic' version of interface. Use smart terminal for the fancy version")
    generator = ClassicInput
    drawer = ClassicDrawer


try:
    with drawer() as drawer:
        with generator(drawer.get_screen(), translator) as input_generator:
            #print("Starting game cycle...")
            drawer.draw(input_generator.buffer)
            for inp in input_generator:
                if inp == "ESCAPE":
                    break
                elif inp in translator:
                    translator[inp]()
                elif len(inp) > 1:
                    game.game_state.execute_action_by_string(inp)
                elif inp.isdigit():
                    game.game_state.execute_action_from_list(int(inp)-1)
                drawer.draw(input_generator.buffer)
except:
    print("Whoops an error happened")
    if DEBUG:
        traceback.print_exc()
        input()
finally:
    print("Exiting...")
    UI.sound.player.stop()






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
