import game
import datetime
import redacted.misc_utilities as utils
from UI.colored_text import ColorString

class Bedroom(game.Location):
    def __init__(self):
        super().__init__()

        @self.object("bed")
        def bed():
            pass

        @bed.action(name="Nap", description="Take a 8 hour nap", time_cost=datetime.timedelta(hours=8), energycost=game.EnergyCost.NONE, color = "magenta", priority = 12)
        def nap():
            game.show_message(ColorString(("You took a nice nap","blue")))
            #utils.sleep()

        @bed.action(name="Sleep", description="Sleep until 7 in the morning", time_cost=datetime.timedelta(), priority = 10)
        def sleep():
            time = game.game_state.time
            if time.hour > 18:
                game.game_state.time = game.game_state.time + datetime.timedelta(days=1)
                game.game_state.time = game.game_state.time.replace(hour=7, minute=0, second=0)
                game.show_message("You slept through the night.")
            elif time.hour < 7:
                game.game_state.time = game.game_state.time.replace(hour=7, minute=0, second=0)
                game.show_message("You slept until the morning.")
            else:
                game.show_message("It is no time to sleep right now.")
            utils.sleep(game.game_state.time - time)

        @self.object("kettle")
        def kettle():
            pass

        @kettle.action(name="Make Instant noodles", time_cost=datetime.timedelta(minutes=5), energycost=game.EnergyCost.NONE, disabled=True)
        def make_instant_noodles():
            utils.eat(self.instant_noodles)
            utils.remove_from_inventory(self.instant_noodles.name)
            game.show_message("You cook some Instant noodles and eat them. The flavoring is a little bit off.")
            self.check_cookable()

        @kettle.action(name="Make Instant soup", time_cost=datetime.timedelta(minutes=5), energycost=game.EnergyCost.NONE, disabled=True)
        def make_instant_soup():
            utils.eat(self.instant_soup)
            utils.remove_from_inventory(self.instant_soup.name)
            game.show_message("You cook a cup of Instant soup. It doesn't taste amazing, but at least it's hot.")
            self.check_cookable()

    def check_cookable(self):
        self.instant_noodles = utils.Food(name='Instant noodles', saturation=.25)
        if utils.is_in_inventory(self.instant_noodles.name):
            self.get_object('kettle').get_action('Make Instant noodles').enable()
        else:
            self.get_object('kettle').get_action('Make Instant noodles').disable()

        self.instant_soup = utils.Food(name='Instant soup', saturation=.3)
        if utils.is_in_inventory(self.instant_soup.name):
            self.get_object('kettle').get_action('Make Instant soup').enable()
        else:
            self.get_object('kettle').get_action('Make Instant soup').disable()

    def when_entering(self, from_location):
        self.check_cookable()
        game.game_state.location = self

class Hallway(game.Location):
    def __init__(self):
        super().__init__()

    def after_action(self, action_executed):
        if game.game_state.time.hour >= 18 or game.game_state.time.hour <= 8:
            game.show_message("Your parents are here")
        else:
            game.show_message("There is no one here")


def init():
    global bedroom, hall
    bedroom = Bedroom()
    hall = Hallway()
    bedroom.add_neighbor(hall)
    bedroom.get_action("Travel to Hallway").priority = 15
    hall.get_action("Travel to Bedroom").priority = 5


init()
def callback():
    pass
game.game_init(bedroom, callback)
