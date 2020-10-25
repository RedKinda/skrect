import game
import datetime


class Bedroom(game.Location):
    def __init__(self):
        super().__init__()
        self.slept = False

        @game.object(name="autizmus", location=self)
        def bed():
            pass

        @bed.action(name="bigschlaf", time_cost=datetime.timedelta(hours=8), description="Take a nice refreshing sleep")
        def sleep():
            game.game_state.show_message("You slept 8 hours")
            bedroom = self

            class Bed(game.Location):
                def __init__(self):
                    super().__init__(description="You are lying in bed")

                    @self.action("put on glasses", time_cost=datetime.timedelta(hours=0))
                    def glasses():
                        game.game_state.show_message("You put on your red glasses")
                        game.game_state.location = bedroom

            game.game_state.location = Bed()



class Bathroom(game.Location):
    def __init__(self):
        super().__init__(description="Bathroom with a few moist windows",
                         desc_when_nearby="You feel wet air coming from this direction")

        @self.action(time_cost=datetime.timedelta(minutes=30))
        def shower():
            game.game_state.show_message("You took a nice refreshing shower!")

    def when_entering(self, from_location):
        game.game_state.show_message("Try typing *shower* to take a shower")
        game.game_state.location = self


class Phone(game.Location):
    def __init__(self):
        super().__init__(name="Phone", description="You are looking at your phone")
        self.original_location = None

        @self.action("close", time_cost=datetime.timedelta(seconds=5))
        def close():
            self.original_location.when_entering(self)
            self.original_location = None

    def when_entering(self, from_location):
        game.game_state.location = self
        self.original_location = from_location







def run():
    bed = Bedroom()
    bath = Bathroom()
    bed.add_neighbor(bath, timecost=datetime.timedelta(seconds=59))

    phone = Phone()



    def callback():
        @game.game_state.action("phone", visible=False)
        def open_phone():
            game.game_state.location.when_leaving(phone)
            phone.when_entering(game.game_state.location)

    game.game_init(bed, callback)

