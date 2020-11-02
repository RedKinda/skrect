import game
import datetime
import random

ENERGY = 16*3600*3

def init_stats():
    game.game_state.init_stat('money', 0)
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

    e = (time/datetime.timedelta(seconds=1))*(energy + 1)
    spend_energy(e)
    spend_hunger(time)
    update_willpower(color)




def sleep(time):
    from redacted.streets.mainroad import encounter_streets
    
    halflife = datetime.timedelta(hours=4)
    e = 1 - game.game_state.get_stat('energy')

    k = .5**(time/halflife)
    game.game_state.set_stat('energy', 1 - k*e)

    for i in encounter_streets:
        i.sleep_reset()

    

def eat(food):
    pass

def spend_energy(amount):
    kmin = 1
    kmax = 2

    hunger = game.game_state.get_stat('hunger')
    e_speed = (1-hunger)*kmax + hunger*kmin

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
    k = .95
    if not weight: return

    outcome = 0
    if color in ['magenta', 'cyan', 'blue', 'white', True]:
        outcome = 1

    kwed = k**weight
    w = kwed*game.game_state.get_stat('willpower') + (1-kwed)*outcome
    game.game_state.set_stat('willpower', w)
