import game
import redacted.shop
import redacted.home
import redacted.school


def run_inits():  # put your init function here
    redacted.home.init()


def run():

    def post_start_init():  # This is for initializations after game is running
        pass

    game.game_init(None, post_start_init)
