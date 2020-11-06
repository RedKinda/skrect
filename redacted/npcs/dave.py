import game
from UI.colored_text import ColorString
import datetime

class Davoid(game.Location):
    def __init__(self):
        super().__init__(description="You are in Dave's personal void. He goes here whenever he is being disobedient.", desc_when_nearby="Visit Dave in his personal void (note: he may not currently be in his personal void).")
        
        @game.object(name="dave", location=self)
        def dave():
            pass

        self.dave = self.get_object("dave")

        @dave.action(name="Talk to Dave", time_cost=datetime.timedelta(minutes=1), description=ColorString(("Dave is very cool because he wears shades. Everyone is very cool because they wear shades in this world, but Dave's shades are somehow cooler. ","red"),("It's because they're not red.","cyan")), energycost = game.EnergyCost.MENTAL, priority = 15)
        def talk():
            dialogue = game.Dialogue("Dave")
            startsit = dialogue.start()

            @startsit.situation("Hello!", response = "Sup.")
            def conversation_begin():

                @conversation_begin.situation("I don't know.", response = "Dave: Neither do I.")
                def idk():
                    pass

                @conversation_begin.situation("What have you been up to?", response = "Dave: I don't know.")
                def idk2():
                    pass
                
    def reload(self):
        from redacted.school import clss
        time = game.game_state.time
        dave = self.dave
        
        if time.weekday() > 4:
            dave.move(self)
        elif time.hour < 6:
            dave.move(self)
        elif time.hour < 8:
            dave.move(clss)
        elif time.hour < 15:
            dave.move(self)
        elif time.hour < 16:
            dave.move(clss)
        else:
            dave.move(self)

dave_void = Davoid()
