import game
import datetime
import random
import redacted.dreams as dreams
from redacted.school import test_date

ENERGY = 24*3600*3

intro_id = 0
def tutorial(action): #action is ignored
    global intro_id
    if intro_id > 6:
        return
    messages = {
        0: "Welcome to REDACTED! To highlight different actions, use your arrow keys. To execute the highlighted action, press the return key.",
        1: "At the top of your screen there are a few informations that will be useful to you. The current date and time is on the left side. Next to that you also see the amount of money you have.",
        2: "Make sure you have enough money ready each sunday, because you need to pay rent. It's a not-so-subtle reminder that your parents would like you to move out.",
        3: "Next to that you can see your total energy and hunger. You can replenish energy by sleeping, and hunger, by, unsurprisingly, eating food. Watch out so you don't run out of energy, or you'll lose.",
        4: "The hungrier you are, the faster your energy drains. Keep that in mind when you're running out of hunger. You can have lunch at school, and you can buy some foods at the Inconvenience store.",
        5: "Speaking of school, you should probably hurry. You should be there by eight. Don't be late. Oh yeah, and you can view the village map by typing map and pressing return.",
        6: "Good luck, Red. We hope you have fun. -ä"
    }
    game.show_message(messages[intro_id])
    intro_id += 1


def init_stats():
    game.game_state.init_stat('money', 40)
    game.game_state.init_stat('energy', .94)
    #game.game_state.init_stat('energy', 0.1)
    game.game_state.init_stat('hunger', .94)
    game.game_state.init_stat('willpower', .2)
    game.game_state.init_stat('infection', 0.)

    game.game_state.init_stat('inventory', [])
    game.game_state.init_stat('seed', random.getrandbits(32))
    game.game_state.init_stat('truth', False)
    game.game_state.init_stat('the_mind', False)
    game.game_state.init_stat('fake_glass', False)

    game.game_state.init_stat("test", "no")

    game.game_state.add_post_action_trigger(update_stats)
    game.game_state.add_post_action_trigger(tutorial)
    tutorial("ä")


def update_stats(action):
    time = action.timecost
    energy = action.energycost
    color = action.color

    spend_stats(time, energy)
    update_willpower(color, weight=1, time=time)




def sleep(time, no_dreams=False):
    if game.game_state.time > test_date.replace(hour = 12, minute = 0, second = 0):
        from redacted.void import endingVoid
        game.game_state.location = endingVoid
    else:
        if no_dreams:
            return realsleep(time)
        if time < datetime.timedelta(hours=6):
            return realsleep(time)

        realsleep(time)
        dreams.dream()



def realsleep(time):
    dreams.infect(time)

    from redacted.streets.mainroad import encounter_streets

    halflife = datetime.timedelta(hours=4)
    e = 1 - game.game_state.get_stat('energy')

    k = .5**(time/halflife)
    game.game_state.set_stat('energy', 1 - k*e)

    game.game_state.set_stat('seed', random.getrandbits(32))
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
        #game.show_message('You have run out of energy! Setting energy to 100%.')
        #new_e = 1.
        from redacted.void import endingVoid
        game.game_state.location = endingVoid
        game.game_state.set_stat('energy', 0)
    game.game_state.set_stat('energy', new_e)

def spend_hunger(time):
    halflife = datetime.timedelta(hours=8)
    hunger = game.game_state.get_stat('hunger')

    k = .5**(time/halflife)
    game.game_state.set_stat('hunger', k*hunger)

def update_willpower(color, weight=1, time=datetime.timedelta(hours=1)):
    time = time/datetime.timedelta(hours=1)
    k = .97
    if not weight: return

    outcome = 0
    if type(color) == float:
        outcome = color
    elif color in ['magenta', 'cyan', 'blue', 'white', True]:
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
