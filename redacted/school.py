import datetime
import game

class Void(game.Location):
    def __init__(self):
        super().__init__(description="You aren't anywhere. There seem to be some objects here with you.")

    def when_entering(self, from_location):
        game.game_state.show_message("As you step through the rift you feel... nothing. Wait... where are you? You shouldn't be here.")

class Hall(game.Location):
    def __init__(self):
        super().__init__(description="You are in the great hall of your school.")

        @game.object(name="flag", location=self)
        def flag():
            pass

        @flag.action(name="Observe flag", time_cost=datetime.timedelta(hours=1), description="A glorious mural.")
        def inspect():
            game.game_state.show_message("On the wall hangs the flag. It makes you feel small.")
            #decrease willpower

    def when_entering(self, from_location):
        if isinstance(from_location, Class):
            game.game_state.show_message("You return to the great hall. Not much has changed.")
        else:
            game.game_state.show_message("You enter the school. On the opposite wall hangs a great flag.")
        game.game_state.location = self

class Class(game.Location):
    def __init__(self):
        super().__init__(description="You are in your class.", desc_when_nearby="You know the way there.")

        @game.object(name="dave", location=self)
        def dave():
            pass

        self.dave = self.get_object("dave")

        @dave.action(name="Talk to Horatio", time_cost=datetime.timedelta(minutes=1), description="As you approach Horatio, you can hear him saying \"Make Horatio great again!\" to thin air.")
        def talk():
            dialogue = game.Dialogue("Perfection.")
            startsit = dialogue.start()

            @startsit.situation("'H...'", response = "Horatio: Come to pry on the most stunning man in the galaxy?")
            def conversation_begin():
                
                @conversation_begin.situation("I was just wondering...", response = "Horatio: Wondering whether you could observe me for just a bit longer? Of course you can, you are my best friend! In the same way a dog is a man's best friend, that is.\nFriendship with Horatio increased!")
                def observe_Horatio():
                    pass

                @conversation_begin.situation("Do you wanna hang out after...", response = "Horatio: After I'm done cloning myself and creating a perfect intergalactic empire? Of course! I'll assign you one of my lesser clones to keep you company.\nFriendship with Horatio increased? Yeah, let's say it increased.")
                def hang_out_with_Horatio_question_mark():
                    pass

                @conversation_begin.situation("Can you stop interrupting me when...", response = "Horatio: No.\nHoratio would hate you now, if he considered your relationship worth remembering its status. And if he actually had a friendship variable.")
                def rekt():
                    pass

        @self.action(name="Attend", time_cost = datetime.timedelta(hours = 1), decription="Attend class until 15.")
        def attend():
            #game.game_state.time.hour = 15
            #game.game_state.time.minutes = 0
            self.reload()
            game.game_state.show_message("You feel refreshingly indocrinated.")

    def reload(self):
        if game.game_state.time.hour < 6:
            game.game_state.show_message("There is no one here.")
            self.dave.move(void)
        elif game.game_state.time.hour < 8:
            game.game_state.show_message("There are a few other students.")
            self.dave.move(self)
        elif game.game_state.time.hour < 15:
            game.game_state.show_message("You are late. The class is in progress.")
            self.dave.move(void)
        elif game.game_state.time.hour < 16:
            game.game_state.show_message("The class just ended, and there are still some students here.")
            self.dave.move(self)
        else:
            game.game_state.show_message("The class is over. No one is here.")
            self.dave.move(void)
            
    def when_entering(self, from_location):
        game.game_state.location = self
        game.game_state.show_message("You enter the class.")
        self.reload()
        
        
def run():
    global void
    
    hall = Hall()
    clss = Class()
    void = Void()
    hall.add_neighbor(clss, timecost=datetime.timedelta(minutes=5))

    def hjalp():
        pass

    game.game_init(hall,hjalp)
