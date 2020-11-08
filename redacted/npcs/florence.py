import game
from UI.colored_text import ColorString
import datetime
import redacted.misc_utilities as utils
import redacted.school as school
import random

class Florence(game.Location):
    def __init__(self, name='Italy'):
        super().__init__(name=name, description="You are in Italy. Wait, there is Italy in the year 2120", desc_when_nearby="How do you travel to Italy? In five minutes?")

        @game.object(name="Florence", location=self)
        def florence():
            pass

        self.florence = self.get_object("Florence")
        self.last_talked_to = datetime.datetime(2120, 5, 1, 7, 0, 0)
        self.friendship = 0.
        self.close_friendship = 0.
        self.topic = random.choice([0, 1, 2])

        @florence.action(name="Talk to Florence", time_cost=datetime.timedelta(minutes=5))
        def talk():
            days = ((game.game_state.time - self.last_talked_to)/datetime.timedelta(days=1))
            self.last_talked_to = game.game_state.time

            self.friendship -= self.close_friendship
            self.close_friendship *= .9**days
            self.friendship *= .75**days
            self.friendship += self.close_friendship

            if self.friendship <= -1:
                game.show_message("Florence does not want to talk to you.")
                return

            if days > 0.5:
                topics = [0, 1, 2]
                self.topic = random.choice(topics)

            l = "I should go."
            dialogue = game.Dialogue("Florence", closable=l)
            startsit = dialogue.start()
            game.show_message("Hi Red, what's up?")
            self.friendship -= 1

            if self.topic == 0: # generic conversation about school
                @startsit.situation("Hey Florence. Not much. You?", response = "Florence: I'm fine, thanks. School's a bit annoying sometimes, but I manage.", closable=l)
                def gschool():
                    self.friendship += 1

                    @gschool.situation("But the teachers are doing their best. I'm glad they are here for us.", response="Florence: Yeah, of course. But it sometimes gets tiring anyway.", color='red', closable=l)
                    def gschool_red():
                        self.friendship -= 1
                        utils.update_willpower('red', weight=6, time=datetime.timedelta(minutes=5))

                        @gschool_red.situation("You've just got to listen to them. They only want us to do well on the test.", response="Florence: Right. Thanks I guess. Uhhh. I've got to go now.", color='red')
                        def gschool_red_red():
                            self.friendship -= 2
                            utils.update_willpower('red', weight=6, time=datetime.timedelta(minutes=5))
                            dialogue.exit()

                        @gschool_red.situation("Yeah. It'd be nice to take a break sometimes.", response="Florence: I'd love to just not go to school sometimes, but my parents won't let me.", closable=l)
                        def gschool_red_white():
                            self.friendship += 1
                            utils.update_willpower('white', weight=3, time=datetime.timedelta(minutes=5))

                            @gschool_red_white.situation("Oh come on. Surely you wouldn't just do something like that? That's wrong.", response="Florence: Right. I didn't mean it that way. Sorry. I should be off.", color='red')
                            def gschool_red_white_red():
                                self.friendship -= 2
                                utils.update_willpower('red', weight=6, time=datetime.timedelta(minutes=5))
                                dialogue.exit()

                            @gschool_red_white.situation("I feel that. My parents wouldn't approve of me doing so either.", response="Florence: Yeah. At least it's our last month in here.", closable=l)
                            def gschool_red_white_white():
                                self.friendship += 1
                                utils.update_willpower('white', weight=3, time=datetime.timedelta(minutes=5))

                        @gschool_red.situation("Sometimes it's better to sleep through it.", response=ColorString(("Ugh yes. It's so boring. ", 'cyan'), "But", (" at least ", 'cyan'), "I", (" pretend to ", 'cyan'), "pay attention", (" so that the teachers don't get angry.", 'cyan')), color='blue', closable=l)
                        def gschool_red_blue():
                            self.friendship += 1
                            utils.update_willpower('blue', weight=3, time=datetime.timedelta(minutes=5))

                    @gschool.situation("I get it. I try to worry about it as little as possible.", response="Florence: That's probably for the best.", closable=l)
                    def gschool_none():
                        self.friendship += 1
                        utils.update_willpower('white', weight=6, time=datetime.timedelta(minutes=5))

                        @gschool_none.situation("...", response="Florence: ... I've got to go now. See you later.")
                        def gschool_none_awkward():
                            self.friendship -= 1
                            dialogue.exit()

            elif self.topic == 1: # generic conversation about the test
                @startsit.situation("Hey Florence. Not much. You?", response="Florence: All good. I was thinking about the test.")
                def gtest():
                    self.friendship += 1

                    @gtest.situation("The test?", response="Florence: The test at the end of the month! I know you forgot the road trip we had, but surely you couldn't have forgotten the thing that's going to affect the rest of your life?", closable=l)
                    def gtest_confused():
                        self.friendship += 1

                        @gtest_confused.situation("Right. The test.", response="Florence: Red, is everything okay? Are YOU okay?", closable=l)
                        def gtest_confused_cont():
                            self.friendship += 1

                            @gtest_confused.situation("Yeah, yeah. I'm fine", response="Florence: Okay. You're a bit confused. I think you should go home and get a good sleep.", closable=l)
                            def gtest_confused_fine():
                                pass

                            if self.friendship < 5:
                                return

                            @gtest_confused.situation("Not really. My parents want me to move out. They make me pay rent every week.", response="Florence: Oh. I'm sorry. I... don't know what to say to that. I hope you can make it through the test. To go to the city.", closable=l)
                            def gtest_close():
                                self.close_friendship += 5
                                self.friendship += 2

                                @gtest_close.situation("Sorry to bother you with this.", response="Florence: No! Don't apologise. It's not your fault.", closable=l)
                                def gtest_close_apology():
                                    pass

                        @gtest_confused.situation("The test?", response="Florence: Yes! The test that decides whether you're going to be able to move to the city. Are you okay Red? You seem a little confused.", closable=l)
                        def gtest_confused_x2():
                            gtest_confused_cont()

                    @gtest.situation("Yeah. It's a bit stressful to know that such an important test is coming.", response="Florence: Exactly. I was thinking, what am I going to do if I don't pass? Do I stay here, in Greatwood?", closable=l)
                    def gtest_yeah():
                        self.friendship += 1

                        if self.close_friendship > 3:
                            game.show_message(ColorString(("Florence: But then again. What even happens in the city? Do I want to go there? I've never heard from anyone who did.", 'blue')))
                            self.friendship += 1
                            utils.update_willpower('white', weight=12, time=datetime.timedelta(minutes=5))

                        @gtest_yeah.situation("I'm going.", response="Florence: Well, that's what everyone thinks. But they never take everyone. Someone always stays behind.", closable=l)
                        def gtest_yeah_going():
                            pass

                        @gtest_yeah.situation("I'm not going.", response="Florence: Really? I thought everyone would want to go. At least they would try.", color='blue', closable=l)
                        def gtest_yeah_notgoing():
                            self.close_friendship += 2
                            self.friendship += 1

            elif self.topic == 2:
                @startsit.situation("Hey Florence. Not much. You?", response="Florence: Yeah, I'm fine. I was actually just thinking about how it's a funny coincidence... Nevermind.", closable=l)
                def gcoincidence():
                    self.close_friendship += 1

                    if game.game_state.get_stat('fake_glass'):
                        @gcoincidence.situation("What?", response=ColorString("Florence: Nothing. I mean it's a little funny how your name is Red, but ", ("not even your glasses are...", 'cyan'), " Like your parents knew. Or they were very wrong."), closable=l)
                        def gcoincidence_name():
                            self.friendship += 1

                            @gcoincidence_name.situation("I... actually picked the name myself.", response="Florence: Oh! I understand. That makes sense. I should have known. Obviously you used a different name before.", closable=l)
                            def gcoincidence_name_myself():
                                self.close_friendship += 1
                                self.friendship += 1

                            @gcoincidence_name.situation("Right.", response="Florence: Yeah. Hm.", closable=l)
                            def gcoincidence_name_right():
                                pass

                    else:
                        @gcoincidence.situation("What?", response="Florence: Nevermind. Nothing.", closable=l)
                        def gcoincidence_name():
                            pass

            @startsit.situation("Hey Florence. I'm glad to be back at school. You?", response="Florence: Well, I'm not.", closable=l)
            def rschool():
                self.close_friendship -= 1
                utils.update_willpower('red', weight=3, time=datetime.timedelta(minutes=5))

    def reload(self):
        from redacted.school import cant
        time = game.game_state.time
        florence = self.florence

        if time.weekday() > 4:
            florence.move(self)
        elif time.hour < 16:
            florence.move(school.cant)
        else:
            florence.move(self)

italy = Florence()
