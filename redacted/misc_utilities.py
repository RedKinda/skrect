import game
import datetime
import random

ENERGY = 16*3600*3

def init_stats():
    game.game_state.init_stat('money', 500)
    game.game_state.init_stat('energy', .5)
    game.game_state.init_stat('hunger', 1.)
    game.game_state.init_stat('willpower', .5)
    game.game_state.init_stat('infection', 0.)

    game.game_state.init_stat('inventory', [])
    game.game_state.init_stat('seed', random.getrandbits(32))

    game.game_state.add_post_action_trigger(update_stats)




def update_stats(action):
    time = action.timecost
    energy = action.energycost
    color = action.color

    spend_stats(time, energy)
    update_willpower(color)




def sleep(time):
    halflife = datetime.timedelta(hours=4)
    e = 1 - game.game_state.get_stat('energy')

    k = .5**(time/halflife)
    game.game_state.set_stat('energy', 1 - k*e)

def eat(food):
    s = food.saturation
    h = 1 - game.game_state.get_stat('hunger')
    game.game_state.set_stat('hunger', 1 - (1 - s)*h)

def spend_stats(time, weight):
    h_start = game.game_state.get_stat('hunger')
    spend_hunger(time)
    h_end = game.game_state.get_stat('hunger')
    h = (h_start + h_end)/2
    spend_energy(time, weight, h=h)

def spend_energy(time, weight, h=None):
    amount = (time/datetime.timedelta(seconds=1))*(weight + 1)
    kmin = 1
    kmax = 2

    if h == None:
        h = game.game_state.get_stat('hunger')
    e_speed = (1-h)*kmax + h*kmin

    e = game.game_state.get_stat('energy')
    new_e = e - e_speed*amount/ENERGY

    if new_e <= 0:
        game.show_message('You have run out of energy! Setting energy to 100%.')
        new_e = 1.
    game.game_state.set_stat('energy', new_e)

def spend_hunger(time):
    halflife = datetime.timedelta(hours=8)
    hunger = game.game_state.get_stat('hunger')

    k = .5**(time/halflife)
    game.game_state.set_stat('hunger', k*hunger)

def update_willpower(color, weight=1):
    k = .98
    if not weight: return

    outcome = 0
    if color in ['magenta', 'cyan', 'blue', 'white', True]:
        outcome = 1

    kwed = k**weight
    w = kwed*game.game_state.get_stat('willpower') + (1-kwed)*outcome
    game.game_state.set_stat('willpower', w)

def add_to_inventory(item):
    inv = game.game_state.get_stat('inventory')
    inv.append(item)
    game.game_state.set_stat('inventory', inv)

def is_in_inventory(item):
    inv = game.game_state.get_stat('inventory')
    return item in inv

def remove_from_inventory(item):
    inv = game.game_state.get_stat('inventory')
    i = inv.pop(inv.index(item))
    game.game_state.set_stat('inventory', inv)




class Food():
    def __init__(self, name, saturation=.5):
        self.name = name
        self.saturation = saturation
