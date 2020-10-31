import game

class Void(game.Location):
    def __init__(self):
        super().__init__(description="You aren't anywhere. There seem to be some objects here with you.")

    def when_entering(self, from_location):
        game.game_state.show_message("As you step through the rift you feel... nothing. Wait... where are you? You shouldn't be here.")

void = Void()
