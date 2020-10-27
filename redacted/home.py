import game
import datetime
import redacted.misc_utilities



class Bedroom(game.Location):
    def __init__(self):
        super().__init__()

        @game.object("bed")
        def bed():
            pass

        @bed.action(name="slep", description="Take a 8 hour nap",  time_cost=datetime.timedelta(hours=8))
        def sleep():
            game.show_message("You took a nice nap")
            sleepfunc()







class Friendshouse(game.Location):
    def __init__(self):
        super().__init__()
