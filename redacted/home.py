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
                utils.sleep(game.game_state.time - time)
            elif time.hour < 7:
                game.game_state.time = game.game_state.time.replace(hour=7, minute=0, second=0)
                utils.sleep(game.game_state.time - time)
            else:
                game.show_message("It is no time to sleep right now.")

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

        @self.action(name = "Pay rent", time_cost = datetime.timedelta(minutes=1), priority = 5, energycost = game.EnergyCost.NONE)
        def pay():
            if utils.spend_money(self.rent_level):
                game.game_state.show_message("You paid your rent for this week.")
                self.last_payment = game.game_state.time.replace(hour = 0, minute = 0, second = 0)
            else:
                game.game_state.show_message("You don't have enough.")

    def after_action(self, action_executed):
        pay = self.get_action("Pay rent")
        if game.game_state.time.hour >= 18 or game.game_state.time.hour <= 8:
            game.show_message("Your parents are here")
            if game.game_state.time.weekday() == 6 and self.last_payment != game.game_state.time.replace(hour = 0, minute = 0, second = 0):
                pay.enabled = True
            else:
                pay.enabled = False
            if self.rent_level == 1:
                from redacted.school import holder
                if holder.sadness_level > 1:
                    self.available = False
                    pay.enabled = False
                    game.game_state.show_message("Your parents know about your behavior regarding school. You are no longer welcome here.")
                elif holder.sadness_level > 0:
                    self.rent_level = 5
                    game.game_state.show_message("Your parents do not seem happy. School must've complained about you. They raised the rent.")
            elif self.rent_level == 5:
                from redacted.school import holder
                if holder.sadness_level > 1:
                    self.available = False
                    pay.enabled = False
                    game.game_state.show_message("Your parents know about your behavior regarding school. You are no longer welcome here.")
        else:
            game.show_message("There is no one here")
            pay.enabled = False

    def when_entering(self, from_location):
        if self.available:
            last_sunday = game.game_state.time - datetime.timedelta(days=(game.game_state.time.weekday()+1))
            last_sunday = last_sunday.replace(hour = 0, minute = 0, second = 0)
            if self.last_payment < last_sunday and from_location != bedroom:
                game.game_state.show_message("It is locked")
                self.available = False
            else:
                game.game_state.location = self
        else:
            game.game_state.show_message("It is locked")



def init():
    global bedroom, hall
    bedroom = Bedroom()
    hall = Hallway()
    bedroom.add_neighbor(hall)
    bedroom.get_action("Travel to Hallway").priority = 15
    hall.get_action("Travel to Bedroom").priority = 10


init()
def callback():
    hall.last_payment = game.game_state.time.replace(hour = 0, minute = 0, second = 0)
    hall.rent_level = 1
    hall.available = True
game.game_init(bedroom, callback)
