import game
import datetime
import redacted.misc_utilities as utils


class Bedroom(game.Location):
    def __init__(self):
        super().__init__()

        @game.object("bed")
        def bed():
            pass

        @bed.action(name="sleep", description="Take a 8 hour nap",  time_cost=datetime.timedelta(hours=8))
        def sleep():
            game.show_message("You took a nice nap")
            utils.sleep()

        @self.object("kettle")
        def kettle():
            pass

        @kettle.action(name="Make noodles", time_cost=datetime.timedelta(minutes=5))
        def make_noodles():
            utils.eat("noodles")


class Hallway(game.Location):
    def __init__(self):
        super().__init__()

    def after_action(self, action_executed):
        if game.game_state.time.hour >= 18 or game.game_state.time.hour <= 8:
            game.show_message("Your parents are here")
        else:
            game.show_message("There is no one here")


def init():
    global bed
    bed = Bedroom()
    hall = Hallway()
    bed.add_neighbor(hall)


def run():
    global bed
    init()
    def callback():
        pass
    game.game_init(bed, callback)