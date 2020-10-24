import game
import datetime


class Bedroom(game.Location):
    def __init__(self):
        super().__init__()

        @game.object(name="bed", location=self)
        def bed():
            pass

        @bed.action(time_cost=datetime.timedelta(hours=8))
        def sleep():
            pass


class Bathroom(game.Location):
    def __init__(self):
        super().__init__()

        @self.location_action(time_cost=datetime.timedelta(minutes=30))
        def shower():
            game.game_state.show_message("You took a nice refreshing shower!")


def run():
    bed = Bedroom()
    bath = Bathroom()
    bed.add_neighbor(bath)
    game.game_init(bed)

