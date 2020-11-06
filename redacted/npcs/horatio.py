import game
from UI.colored_text import ColorString
import datetime

class Horatio_Prime(game.Location):
    def __init__(self):
        super().__init__(description="You are on the Horatio homeworld, Horatio Prime.", desc_when_nearby="Travel to Horatio Prime, as the name of this action suggests.")
        
        @game.object(name="horatio", location=self)
        def horatio():
            pass

        self.horatio = self.get_object("horatio")

        @horatio.action(name="Talk to Horatio", time_cost=datetime.timedelta(minutes=1), description="As you approach Horatio, you can hear him saying \"Make Horatio great again!\" to thin air.", energycost = game.EnergyCost.HEAVY, priority = 10)
        def talk():
            dialogue = game.Dialogue("Perfection.")
            startsit = dialogue.start()

            @startsit.situation("'H...'", response = "Horatio: Come to pry on the most stunning man in the galaxy?")
            def conversation_begin():

                @conversation_begin.situation("I was just wondering...", response = "Horatio: Wondering whether you could observe me for just a bit longer? Of course you can, you are my best friend! In the same way a dog is a man's best friend, that is.\nFriendship with Horatio increased!")
                def observe_Horatio():
                    pass

                @conversation_begin.situation("Do you wanna hang out after...", response = "Horatio: After I'm done cloning myself and creating a perfect intergalactic empire? Of course! I'll assign you one of my lesser clones to keep you company.\nFriendship withHoratio increased? Yeah, let's say it increased.")
                def hang_out_with_Horatio_question_mark():
                    pass

                @conversation_begin.situation("Can you stop interrupting me when...", response = "Horatio: No.\nHoratio would hate you now, if he considered your relationship worth remembering its status. And if he actually had a friendship variable.")
                def rekt():
                    pass

                
    def reload(self):
        from redacted.school import clss
        time = game.game_state.time
        horatio = self.horatio
        
        if time.weekday() > 4:
            horatio.move(self)
        elif time.hour < 16:
            horatio.move(self)
        else:
            horatio.move(clss)

horatio_prime = Horatio_Prime()
