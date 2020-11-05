import game
import datetime
import random
import redacted.dreams as dreams
from redacted.school import test_date

ENERGY = 16*3600*3

def init_stats():
    game.game_state.init_stat('money', 500)
    game.game_state.init_stat('energy', 1.)
    game.game_state.init_stat('hunger', 1.)
    game.game_state.init_stat('willpower', .5)
    game.game_state.init_stat('infection', 0.)

    game.game_state.init_stat('inventory', [])
    game.game_state.init_stat('seed', random.getrandbits(32))
    game.game_state.init_stat('truth', False)
    game.game_state.init_stat('fake_glass', False)

    game.game_state.init_stat("test", "no")

    game.game_state.add_post_action_trigger(update_stats)




def update_stats(action):
    time = action.timecost
    energy = action.energycost
    color = action.color

    spend_stats(time, energy)
    update_willpower(color, weight=1, time=time)




def sleep(time, no_dreams=False):
    if game.game_state.time > test_date.replace(hour = 12, minute = 0, second = 0):
        test = game.game_state.get_stat("test")
        if test == "infected":
            game.game_state.show_message("Failure. You are going to quarantine. For all of eternity. Congratulations!")
        elif test == "passed":
            game.game_state.show_message("Ending achieved! You are going to Brazil.")
        else:
            game.game_state.show_message("Ending achieved! You remain in your home village. You are stuck here. At your home. You are stuck, at home. You could say you're stuck home.")
    if no_dreams:
        return realsleep(time)
    if time < datetime.timedelta(hours=6):
        return realsleep(time)

    dreams.dream()
    realsleep(time)


def realsleep(time):
    from redacted.streets.mainroad import encounter_streets

    halflife = datetime.timedelta(hours=4)
    e = 1 - game.game_state.get_stat('energy')

    k = .5**(time/halflife)
    game.game_state.set_stat('energy', 1 - k*e)

    for i in encounter_streets:
        i.sleep_reset()

def eat(food):
    s = food.saturation
    h = 1 - game.game_state.get_stat('hunger')
    game.game_state.set_stat('hunger', 1 - (1 - s)*h)

def update_infection(amount):
    i = game.game_state.get_stat('infection')
    i += amount
    if i < 0: i = 0
    elif i > 1: i = 1
    game.game_state.set_stat('infection', i)

def spend_money(amount):
    if type(amount) != int:
        raise TypeError('Amount of money to spend must be an integer')
    money = game.game_state.get_stat('money')

    if amount > money:
        return False

    game.game_state.set_stat('money', money - amount)
    return True

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

def update_willpower(color, weight=1, time=datetime.timedelta(hours=1)):
    time = time/datetime.timedelta(hours=1)
    k = .95
    if not weight: return

    outcome = 0
    if color in ['magenta', 'cyan', 'blue', 'white', True]:
        outcome = 1

    kwed = k**weight
    kted = kwed**time
    w = kted*game.game_state.get_stat('willpower') + (1-kted)*outcome
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
