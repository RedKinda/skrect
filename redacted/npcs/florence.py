import game
from UI.colored_text import ColorString
import datetime
import redacted.misc_utilities as utils
from redacted.school import cant

class Italy(game.Location):
    def __init__(self, name='Italy'):
        super().__init__(name=name, description="You are in Italy. Wait, there is Italy in the year 2220", desc_when_nearby="How do you travel to Italy? In five minutes?")

        @game.object(name="Florence", location=self)
        def florence():
            pass

        self.florence = self.get_object("Florence")

        @horatio.action(name="Talk to Florence", time_cost=datetime.timedelta(minutes=5))
        def talk():
            dialogue = game.Dialogue("Florence")
            startsit = dialogue.start()
            game.show_message("Hi Red, what's up?")
            l = "Sorry. I've got to go now."

            # generic conversation
            @startsit.situation("Hey Florence. Not much. You?", response = "Florence: I'm fine, thanks. School's a bit annoying sometimes, but I manage.", closable=l)
            def g1():

                @g1.situation(ColorString(("But the teachers are doing their best. I'm glad they are here for us.", 'red')), response="Florence: Yeah, of course. But it sometimes gets tiring anyway.", closable=l)
                def g1_red():
                    utils.update_willpower('red', weight=6, time=datetime.timedelta(minutes=5))

                    @g1_red.situation(ColorString(("You've just got to listen to them. They only want us to do well on the test.", 'red')), response="Florence: Right. Thanks I guess. Uhhh. I've got to go now.", closable=l)
                    def g1_red_red():
                        utils.update_willpower('red', weight=6, time=datetime.timedelta(minutes=5))
                        dialogue.exit()

                    @g1_red.situation("Yeah. It'd be nice to take a break sometimes.", response="Florence: I'd love to just not go to school sometimes, but my parents won't let me.", closable=l)
                    def g1_red_white():
                        utils.update_willpower('white', weight=3, time=datetime.timedelta(minutes=5))

                        @g1_red_white.situation(ColorString(("Oh come on. Surely you wouldn't just do something like that? That's wrong.", 'red')), response="Florence: Right. I didn't mean it that way. Sorry. I should be off.")
                        def g1_red_white_red():
                            utils.update_willpower('red', weight=6, time=datetime.timedelta(minutes=5))
                            dialogue.exit()

                        @g1_red_white.situation("I feel that. My parents wouldn't approve of me doing so either.", response="Florence: Yeah. At least it's our last month in here.", closable=l)
                        def g1_red_white_white():
                            utils.update_willpower('white', weight=3, time=datetime.timedelta(minutes=5))

                        @g1_red_white.situation("Luckily there's only a month left.", response="Florence: Hopefully it is over as soon as possible.", closable=l)
                        def red_white_none():
                            pass

                    @g1_red.situation("Sometimes it's better to sleep through it.", response="Ugh yes. It's so boring. But at least I pretend to pay attention so that the teachers don't get angry.", closable=l)
                    def g1_red_blue():
                        utils.update_willpower('blue', weight=3, time=datetime.timedelta(minutes=5))

                @g1.situation("I get it. I try to worry about it as little as possible too.", response="Florence: aaaaaaaaaaaaaaaaaaaaaaaaaaaa neivem co sem mam napisat", closable=l)


    def reload(self):
        from redacted.school import clss
        time = game.game_state.time
        florence = self.florence

        if time.weekday() > 4:
            florence.move(self)
        elif time.hour < 16:
            florence.move(self)
        else:
            florence.move(cant)

italy = Italy()
