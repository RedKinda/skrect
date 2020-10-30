import datetime
import game

class Sadness():
    def __init__(self):
        self.sadness = 0

def resolve_sadness():
    today = game.game_state.time
    today = today.replace(hour=0, minute=0, second=0)
    days_missed = today - last_visit
    days_missed = days_missed.days - 1
    den = today.weekday()
    remainder = days_missed % 7
    days_missed //= 7
    days_missed *= 5
    days_missed += min(den, remainder) + max(0, remainder - den - 2)
    if den == 6:
        days_missed -= 1
    #game.game_state.show_message("You last visited school on " + str(last_visit) + " and today is " + str(today))
    #game.game_state.show_message("You missed " + str(today - last_visit) + ", therefore the result is " + str(days_missed))
    return days_missed

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
            game.game_state.show_message("On the wall hangs the flag. It makes you feel small. Your sadness value is " + str(sadness.sadness))
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
        self.distance = datetime.timedelta(minutes=5)
        self.horatio_speech = datetime.timedelta(minutes=1)

        @dave.action(name="Talk to Horatio", time_cost=datetime.timedelta(minutes=1), description="As you approach Horatio, you can hear him saying \"Make Horatio great again!\" to thin air.")
        def talk():
            self.reload(game.game_state.time + self.horatio_speech)
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

        @self.action(name="Attend", time_cost = datetime.timedelta(0), description="Attend class until 15.")
        def attend():
            global last_visit
            days_missed = resolve_sadness()
            sadness.sadness += days_missed*2
            if days_missed > 0:
                sadness.sadness -= 1
            #game.game_state.show_message("Lessons missed: " + str(days_missed))
            game.game_state.show_message("WARNING: SOMETHING MAY HAPPEN TO THE SADNESS VALUE IF YOU PRESS \"GOODBYE\" NOW. DO NOT DO IT! IT IS NOT A FEATURE.")
            last_visit = game.game_state.time
            last_visit = last_visit.replace(hour=0, minute=0, second=0)
            
            #this should not be exitable
            lesson = game.Dialogue("Attending a lesson.")
            startsit = lesson.start()

            @startsit.situation("Pay close attention", response = "Here will be lore.", closable = False)
            def lesson_attention():
                #decrease willpower
                sadness.sadness = max(0, sadness.sadness-1)
                lesson_done()

            @startsit.situation("Don't", response = "Haha, I just realized Horatio looks like Meme Man.", closable = False)
            def lesson_funni():
                lesson_done()

            @startsit.situation("Sleep", response = "You slept in class. The teacher is not happy.", closable = False)
            def lesson_schlaf():
                #decrease tiredness slightly
                sadness.sadness += 1
                lesson_done()

            def lesson_done():
                @lesson.situation("Wait for the end.", response = "You attended all of the lesson.", closable = False)
                def lesson_end():
                    game.game_state.time = datetime.datetime(game.game_state.time.year, game.game_state.time.month, game.game_state.time.day, 15, 0, 0)
                    if sadness.sadness > 5:
                        game.game_state.show_message("You can tell from the way the teacher looks at you before they leave the class that you're walking on thin ice.")
                    self.reload(game.game_state.time)
                    lesson.exit()
            
    def reload(self, new_time):
        
        attend = self.get_action("Attend")
        escape = self.get_action("Travel to Hall")
        dave = self.dave

        if new_time.weekday() > 4:
            game.game_state.show_message("There is no one here. No school during weekend.")
            dave.move(void)
            attend.enabled = False
            escape.enabled = True
        elif new_time.hour < 6:
            game.game_state.show_message("There is no one here yet.")
            dave.move(void)
            attend.enabled = True
            escape.enabled = True
        elif new_time.hour < 8:
            game.game_state.show_message("There are a few other students. The class will start soon.")
            dave.move(self)
            attend.enabled = True
            escape.enabled = True
        elif new_time.hour < 15:
            game.game_state.show_message("You are late. The class is in progress.")
            
            days_missed = resolve_sadness()
            sadness.sadness += 1
            
            if days_missed > 0:
                game.game_state.show_message("The teacher is not happy with you. If you skip school too much, your parents will know.")

            dave.move(void)
            attend.enabled = True
            escape.enabled = False
        elif new_time.hour < 16:
            game.game_state.show_message("The class just ended, and there are still some students here.")
            dave.move(self)
            attend.enabled = False
            escape.enabled = True
        else:
            game.game_state.show_message("The class is over. No one is here.")
            dave.move(void)
            attend.enabled = False
            escape.enabled = True
               
    def when_entering(self, from_location):
        game.game_state.location = self
        game.game_state.show_message("You enter the class.")
        new_time = game.game_state.time + self.distance
        self.reload(new_time)
        
        
def run():
    global void, hall, sadness

    sadness = Sadness()
    
    hall = Hall()
    clss = Class()
    void = Void()
    hall.add_neighbor(clss, timecost=clss.distance)

    def visit_init():
        global last_visit
        last_visit = game.game_state.time
        last_visit -= datetime.timedelta(days = 1)
        last_visit = last_visit.replace(hour=0, minute=0, second=0)

    game.game_init(hall,visit_init)
