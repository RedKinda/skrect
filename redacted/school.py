import datetime
import game
from UI.colored_text import ColorString
from redacted.void import void
import redacted.misc_utilities as utils
from redacted.npcs.dave import dave_void
from redacted.npcs.horatio import horatio_prime
from redacted.npcs.florence import italy


class Holder():
    def __init__(self):
        self.sadness = 0
        self.sadness_level = 0

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

class Hall(game.Location):
    def __init__(self):
        super().__init__(description="You are in the great hall of your school.")

        #@game.object(name="flag", location=self)
        #def flag():
        #    pass

        #@flag.action(name="Observe flag", time_cost=datetime.timedelta(seconds=10), description="A glorious mural.", energycost = game.EnergyCost.NONE, priority = 5, color = "red")
        #def inspect():
        #    game.game_state.show_message("On the wall hangs the flag. It makes you feel small.")
            #decrease willpower

        @game.object(name="notice board", location=self)
        def bored():
            pass

        @bored.action(name="Inspect testing announcement", time_cost=datetime.timedelta(seconds=10), description="Your grade will all be tested for special abilities soon. As every year.")
        def test_announcement():
            game.game_state.show_message(ColorString(("Attention! All students of grade 12 will be tested on the 31st of May 2120. Good results on the test will result in relocation to the Capital City and a place at the Higher Education Institute. Participation is highly recommended.","red")))

        @bored.action(name="Inspect effectivity measures announcement", time_cost=datetime.timedelta(seconds=10), description="These were estabilished rather recently.")
        def effectivity_announcement():
            game.game_state.show_message(ColorString(("Attention! The Government recommends following measures to ensure that workplace effectivity is at its maximum:\nMinimalize chatting\nAbsolutely NO art in any way, shape or form\nDo not read text you don't trust\nDo not observe imagery you do not trust","red")))

    def when_entering(self, from_location):
        if isinstance(from_location, Class):
            game.game_state.show_message("You return to the great hall. Not much has changed.")
        else:
            game.game_state.show_message("You enter the school. On the opposite wall hangs a great flag.")
        game.game_state.location = self

class Canteen(game.Location):
    def __init__(self):
        super().__init__(description="You are in the school canteen.", desc_when_nearby="The food is not good, but still better than home.")

        self.distance = datetime.timedelta(minutes=1)

        @self.action(name="Eat lunch", time_cost=datetime.timedelta(minutes=30), energycost=game.EnergyCost.NONE, priority = 5, color = "yellow")
        def eat():
            #eat
            game.game_state.show_message("The food is edible.")
            self.last_lunch = game.game_state.time.replace(hour=0,minute=0,second=0)
            lunch = utils.Food(name = "Canteen lunch", saturation = .5)
            utils.eat(lunch)

    def after_action(self, action_executed):
        time = game.game_state.time
        if (time.hour < 14 or time.hour > 15) or time.weekday() > 4:
            self.get_action("Eat lunch").disable()
            game.game_state.show_message("Lunch is not being served right now.")
        elif self.last_lunch < time.replace(hour=0,minute=0,second=0):
            self.get_action("Eat lunch").enable()
            game.game_state.show_message("You're in time for lunch.")
            game.game_state.show_message(str(self.last_lunch))
        else:
            self.get_action("Eat lunch").disable()
            game.game_state.show_message("You already had your lunch today.")

        #reload NPCs
        italy.reload()

class Class(game.Location):
    def __init__(self):
        super().__init__(description="You are in your class.", desc_when_nearby="You know the way there.")

        @self.action(name="Attend", time_cost = datetime.timedelta(0), description="Attend class until 15.", priority = 5, color = "yellow")
        def attend():
            global last_visit
            days_missed = resolve_sadness()
            holder.sadness += days_missed*2
            if days_missed > 0:
                holder.sadness -= 1
            #game.game_state.show_message("Lessons missed: " + str(days_missed))
            #game.game_state.show_message("WARNING: SOMETHING MAY HAPPEN TO THE SADNESS VALUE IF YOU PRESS \"GOODBYE\" NOW. DO NOT DO IT! IT IS NOT A FEATURE.")
            last_visit = game.game_state.time
            last_visit = last_visit.replace(hour=0, minute=0, second=0)
            startTime = datetime.datetime(game.game_state.time.year, game.game_state.time.month, game.game_state.time.day, 8, 0, 0)
            endTime = datetime.datetime(game.game_state.time.year, game.game_state.time.month, game.game_state.time.day, 15, 0, 0)

            #this should not be exitable
            lesson = game.Dialogue("Attending a lesson.", closable = False)
            startsit = lesson.start()

            @startsit.situation("Pay close attention", response = ColorString(("You discussed the importance of Lens and how they increase performance. Did you know that if you don't wear them, there's a high chance you will die?", "red"), ("The Government will make sure of that.", "cyan")), closable = False, color = "red")
            def lesson_attention():
                holder.sadness = max(0, holder.sadness-1)
                if game.game_state.time.hour < 8:
                    utils.spend_stats(startTime - game.game_state.time, game.EnergyCost.NONE)
                    timePoint = startTime
                else:
                    timePoint = game.game_state.time
                utils.spend_stats(endTime - timePoint, game.EnergyCost.MENTAL)
                utils.update_willpower(False, time=(endTime-timePoint))
                lesson_done()

            @startsit.situation("Don't", response = "Haha, I just realized Horatio looks like Meme Man.", closable = False, color = "cyan")
            def lesson_funni():
                utils.spend_stats(endTime - game.game_state.time, game.EnergyCost.NONE)
                #holder.sadness += 10
                lesson_done()

            @startsit.situation("Sleep", response = "You slept in class. The teacher is not happy.", closable = False, color = "blue")
            def lesson_schlaf():
                utils.sleep((endTime - game.game_state.time)*0.5)

                holder.sadness += 1
                lesson_done()

            def lesson_done():
                @lesson.situation("Wait for the end.", response = "It is time for a late lunch.", closable = False)
                def lesson_end():
                    game.game_state.time = endTime
                    if holder.sadness >= 15:
                        holder.sadness_level = 2
                        game.game_state.show_message("You've crossed the line. Your parents will know.")
                    elif holder.sadness >= 10:
                        if holder.sadness_level == 0:
                            holder.sadness_level = 1
                        game.game_state.show_message("You can tell from the way the teacher looks at you before leaving the class that you're standing on thin ice.")
                    elif holder.sadness >= 5:
                        game.game_state.show_message("The teacher does not appear happy with you. You should be more careful.")
                    lesson.exit()

        @self.action(name="Attend testing", time_cost = datetime.timedelta(0), description="Attend the special testing until 15.", priority = 5, color = "yellow")
        def attend():
            global last_visit
            days_missed = resolve_sadness()
            holder.sadness += days_missed*2
            if days_missed > 0:
                holder.sadness -= 1
            #game.game_state.show_message("Lessons missed: " + str(days_missed))
            #game.game_state.show_message("WARNING: SOMETHING MAY HAPPEN TO THE SADNESS VALUE IF YOU PRESS \"GOODBYE\" NOW. DO NOT DO IT! IT IS NOT A FEATURE.")
            last_visit = game.game_state.time
            last_visit = last_visit.replace(hour=0, minute=0, second=0)
            startTime = datetime.datetime(game.game_state.time.year, game.game_state.time.month, game.game_state.time.day, 8, 0, 0)
            endTime = datetime.datetime(game.game_state.time.year, game.game_state.time.month, game.game_state.time.day, 15, 0, 0)

            #this should not be exitable
            lesson = game.Dialogue("Doing the test.", closable = False)
            startsit = lesson.start()

            @startsit.situation("Do your best", response = ColorString(("You completed the test. Results should come soon.", "yellow"), (" The questions were really odd. Some of them didn't seem to even have anything in common with mental strength...\n\nMaybe they're testing for something else?", "cyan")), closable = False, color = "red")
            def lesson_attention():
                if game.game_state.time.hour < 8:
                    utils.spend_stats(startTime - game.game_state.time, game.EnergyCost.NONE)
                    timePoint = startTime
                else:
                    timePoint = game.game_state.time
                utils.spend_stats(endTime - timePoint, game.EnergyCost.MENTAL)
                game.game_state.set_stat("test", "passed")
                lesson_done()

            @startsit.situation("Don't", response = ColorString(("You failed the test on purpose. Well, you hope you did? It was really strange.","blue")), closable = False, color = "blue")
            def lesson_funni():
                if game.game_state.time.hour < 8:
                    utils.spend_stats(startTime - game.game_state.time, game.EnergyCost.NONE)
                    timePoint = startTime
                else:
                    timePoint = game.game_state.time
                utils.spend_stats(endTime - timePoint, game.EnergyCost.TRAVEL)
                #holder.sadness += 10
                lesson_done()

            def lesson_done():
                @lesson.situation("Wait for the end.", response = "It is time for a late lunch.", closable = False)
                def lesson_end():
                    game.game_state.time = endTime
                    if game.game_state.get_stat("infection") > 0.1:
                        game.game_state.set_stat("test", "infected")
                    lesson.exit()

    def when_entering(self, from_location):
        game.game_state.location = self
        game.game_state.show_message("You enter the class.")

    def after_action(self, action_executed):
        attend = self.get_action("Attend")
        escape = self.get_action("Travel to Hall")
        test = self.get_action("Attend testing")
        time = game.game_state.time

        if time.weekday() > 4:
            game.game_state.show_message("There is no one here. No school during weekend.")
            attend.enabled = False
            escape.enabled = True
        elif time.hour < 6:
            game.game_state.show_message("There is no one here yet.")
            attend.enabled = True
            escape.enabled = True
        elif time.hour < 8:
            game.game_state.show_message("There are a few other students. The class will start soon.")
            attend.enabled = True
            escape.enabled = True
        elif time.hour < 15:
            game.game_state.show_message("You are late. The class is in progress.")
            days_missed = resolve_sadness()
            holder.sadness += 1

            if days_missed > 0:
                game.game_state.show_message("You should be careful. If you skip school too much, your parents will know.")

            attend.enabled = True
            escape.enabled = False
        elif time.hour < 16:
            game.game_state.show_message("The class just ended, and there are still some students here.")
            attend.enabled = False
            escape.enabled = True
        else:
            game.game_state.show_message("The class is over. No one is here. Except for Horatio, for some reason.")
            attend.enabled = False
            escape.enabled = True

        test.disable()
        if test_date == time.replace(hour = 0, minute = 0, second = 0):
            if attend.enabled:
                attend.disable()
                test.enable()

        dave_void.reload()
        horatio_prime.reload()

#this function is no longer used hopefully? I dont know how to phrase this
#def reload(new_time):
#    dave = clss.dave
#    joey = clss.joey
#    jane = clss.jane
#    horatio = clss.horatio

    #if new_time.weekday() > 4:
    #    dave.move(void)
    #    joey.move(void)
    #    jane.move(void)
    #    horatio.move(clss)
    #elif new_time.hour < 6:
    #    dave.move(void)
    #    joey.move(void)
    #    jane.move(void)
    #    horatio.move(void)
    #elif new_time.hour < 8:
    #    dave.move(clss)
    #    joey.move(clss)
    #    jane.move(clss)
    #    horatio.move(clss)
    #elif new_time.hour < 15:
    #    dave.move(void)
    #    joey.move(void)
    #    jane.move(void)
    #    horatio.move(void)
    #elif new_time.hour < 16:
    #    dave.move(clss)
    #    joey.move(cant)
    #    jane.move(cant)
    #    horatio.move(void)
    #else:
    #    dave.move(void)
    #    joey.move(void)
    #    jane.move(void)
    #    horatio.move(void)



holder = Holder()

hall = Hall()
clss = Class()
cant = Canteen()
hall.add_neighbor(clss, timecost=datetime.timedelta(minutes=1))
hall.add_neighbor(cant, timecost=datetime.timedelta(minutes=1))
hall.get_action("Travel to Class").priority = 10
hall.get_action("Travel to Canteen").priority = 15

test_date = datetime.datetime(year = 2120, month = 5, day = 31, hour = 0, minute = 0, second = 0)

def visit_init():
    global last_visit
    last_visit = game.game_state.time
    last_visit -= datetime.timedelta(days = 1)
    last_visit = last_visit.replace(hour=0, minute=0, second=0)
    cant.last_lunch = game.game_state.time.replace(hour=0, minute=0, second=0) - datetime.timedelta(days=1)

def run():
    game.game_init(hall, visit_init)
