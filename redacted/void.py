import game
import datetime
from UI.colored_text import ColorString

class Void(game.Location):
    def __init__(self):
        super().__init__(description="You aren't anywhere. There seem to be some objects here with you.")

    def when_entering(self, from_location):
        game.game_state.show_message("As you step through the rift you feel... nothing. It didn't even let you pass.")

class Ending(game.Location):
    def __init__(self):
        super().__init__(description="AN ENDING")

        @self.action(name="Anticipate", time_cost = datetime.timedelta(0))
        def proceed():
            #game.game_state.show_message(str(game.game_state.get_stat("energy")))
            if game.game_state.get_stat("energy") <= 0:
                game.game_state.show_message("You have neglected yourself far too much. Your body can hardly sustain itself. You have failed.")
                game.game_state.show_message("GAME OVER")
            else:
                if game.game_state.get_stat("infection") > 0.1:
                    status = (" (green)","green")
                elif game.game_state.get_stat("fake_glass"):
                    status = (" (blue)","blue")
                else:
                    status = (" (red)","red")
                if game.game_state.get_stat("test") == "infected":
                    ending = "3"
                    game.game_state.show_message(ColorString(("Instead of the results, you get surprised with several enforcers at your doorstep. They don't even tell you what's wrong. You are taken and transported to an unfamiliar room. You stay here for longer than you can keep track of. ","white"),("They knew. This was more than a skill test. ","cyan"),("Dangerous ","yellow"),("individuals ","red"),("and their Art ","green"),("must be eliminated.","red")))
                elif game.game_state.get_stat("test") == "passed":
                    ending = "2"
                    game.game_state.show_message(ColorString(("You are chosen. Your abilities need to be developed further. ","red"),("You depart the town on a train directly to the Capital City. ","white"),("You're scared. You're suddenly moving from everything you've ever known. But ","cyan"),("you believe your life there will be much better than anything you could've had at home.","magenta")))
                else:
                    ending = "1"
                    game.game_state.show_message(ColorString(("The train departs without you. Were you not good enough? ","white"),("Or were you good enough and they weren't? ","blue"),("You are stuck here, for now. At your home village. Yes. Stuck home at your uneventful village. ","red"),("But maybe this is not the end? The village is uneventful, but not necessarily for long...","cyan")))
                game.game_state.show_message(ColorString(("ENDING "+ending+"/3","white"),(status)))
                game.game_state.show_message("Thank you for playing. If the full game ever exists, the story will continue.")
            self.get_action("Anticipate").disable()

    def when_entered(self, from_location):
        game.game_state.show_message("The test is evaluated as you sleep. The results will come soon.")


endingVoid = Ending()

void = Void()
