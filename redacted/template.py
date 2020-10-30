import game
import datetime
import redacted.misc_utilities

class Roomname(game.Location):
    def __init__(self):
        super().__init__()

def run():
    room = Roomname()

    def callback():
        pass

    game.game_init(room, callback)
