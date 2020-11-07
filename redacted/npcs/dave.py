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
        self.dave.progression = 0
        #0 - almost normal
        #1 - likes his art a lot
        #2 - a bit too obsessed
        #3 - does not even hide it anymore
        #4 - absent, will leave the player the key to his room for extra plot

        self.dave.hang_out_day = datetime.datetime(1,1,1,0,0,0)

        @dave.action(name="Talk to Dave", time_cost=datetime.timedelta(minutes=1), description=ColorString(("Dave is very cool because he wears shades. Everyone is very cool because they wear shades in this world, but Dave's shades are somehow cooler. ","red"),("It's because they're not red.","cyan")), energycost = game.EnergyCost.MENTAL, priority = 15)
        def talk():
            dialogue = game.Dialogue("Dave")
            startsit = dialogue.start()

            greetings = ["Sup.",ColorString(("Sup. ","white"),("Do you want to hear something cool I wrote?","green")),ColorString(("Hello friend. ","white"),("Are you here to check out my work?","green")),ColorString(("Read my poetry. It is very moving. You'll love it. You can't miss out on this.","green"))]
            greeting = ColorString(("Dave: ","white")) + greetings[self.dave.progression]
            
            @startsit.situation("Hello!", response = greeting)
            def conversation_begin():

                from redacted.school import clss
                if self.dave.location == clss and self.dave.progression < 3:
                    game.game_state.show_message(ColorString(("I see we have something in common. Maybe we could talk in privacy later?","cyan")))

                events = ["This is not a line you should see ingame. I shouldn't be saying this. Are you sure you hadn't broken anything?",
                          "You know, nothing special. You should keep talking to me every day in case somehing new happens. That was a joke. But that doesn't mean you can't do that.",
                          "What do you think of the new measures? They seem weird, I don't see how banning art is supposed to improve work quality.",
                          "It's gonna be weekend again tomorrow. Finally.",
                          
                          "Don't mind me, just enjoying a saturday in the park. It's very nice out there.",
                          "You know, all this nature, it almost speaks to me. I feel a desire to do something. But what?",
                          
                          "School again. Back to normal.",
                          ColorString(("I've been thinking and I think I finally know. ","white"),("I'm gonna try writing something. I'm gonna do art.","green")),
                          ColorString(("They think they know best. ","white"),("Well they can't stop me from writing.","green")),
                          "The angular buildings, the towering shadows.",
                          "I've had quite a strange dream tonight. Something about... You know what? Forget it.",

                          "The trees and the grass, so beautiful!",
                          "I'm constantly being inspired to do something more.",

                          ColorString(("School again. Back to normal. Once again. ","white"),("I will write about this sometime.","green")),
                          "I've been stargazing, it's really nice.",
                          ColorString(("Have you seen it? The sunrise was so fascinating today. ","white"),("My poems are forever changed.","green")),
                          "My dreams are really inspiring. I've tried to ignore them at first, but they are too interesting.",
                          "The lighting is so contrasting, I can't pay attention to anything else, I can only continue looking.",

                          "The grass consists of so many individual grasses, but these grasses are making what is greater than only grasses, that is grass.",
                          "I'm done with it. Everyone will know! I can't hide it, it's too strong, that would be selfish because They It is We are the Message is more important than me.",

                          ColorString(("I am writing about my dreams, about our dreams, there is much to be done, to share, to show the world, even if the ones in power do not want that. ","white"),("I was afraid of this, I didn't want this, but am I truly insane, am I just right? Is it a blessing or a curse because I genuinely don't know I just want to write and I want everyone to hear.","blue")),
                          ColorString(("It is my Our purpose to do this, because only then will I We have purpose. ","white"),("But I'm not sure and I don't know if I am even still alive or if I am too far gone, if They have consumed me and I am no longer. I have to share my thoughts on this.","blue")),
                          ColorString(("You too will love my poetry, my words, spoken with knowledge all should hear, it is beautiful and makes all that sense, and I will show you everything. ","white"),("I could have prevented this, I could have been more careful, I never should have put it down, but then, what would I have remained? Still a puppet, but someone else's.","blue")),
                          ColorString(("The town knows and it sees knows that I am here and We too with me Us we bring you and Us peace and harmony and all that beauty and we cannot stop now, it is only beginning. ","white"),("Why even try. It's too strong. Save yourself. Just forget me. They'll make sure.","blue")),
                          "I am writing EVERYTHING down, but BETTER! I don't need sleep sustenance material needs as well, because that is temporary and disappears, but THIS will STAY and EVERYONE will HEAR, EVERYONE will KNOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                          
                    ]
                event = ColorString(("Dave: ","white")) + events[game.game_state.time.day]
                @conversation_begin.situation("How's life?", response = event)
                def daily():
                    pass
                if self.dave.location == clss:
                    if self.dave.progression < 3:
                        dave_wait = "Dave: Good idea, I'll be waiting in the park. See you there."
                    else:
                        dave_wait = "Dave: Why? Why would I show you it everything then when I can show you EVERYTHING here?"
                    
                    @conversation_begin.situation("Shall we hang out after school?", response = dave_wait)
                    def idk2():
                        if self.dave.progression < 3:
                            self.dave.hang_out_day = game.game_state.time.replace(hour=0,minute=0,second=0)

                from redacted.streets.greatwood import greatwood_park as park
                if self.dave.location == park or self.dave.progression == 3:
                    if self.dave.progression < 3:
                        dave_response = ColorString(("I found these glasses in the forest on the ground. I didn't really think about it but I put them on and everyhting was different. Now I can't really wear the red ones anymore, everything is so dark. Sometimes I just straight up can't do something. It's weird.","cyan"))
                    else:
                        dave_response = ColorString(("I couldn't see anything, but NOW it is obvious, and We It will give everyone a pair, so they can read ALL the word I We will write! EVERYONE.","green"))
                    @conversation_begin.situation("Discuss stuff you couldn't otherwise.", response = dave_response, color="cyan")
                    def forbidden():
                        pass
                
    def reload(self):
        from redacted.school import clss
        from redacted.streets.greatwood import greatwood_park as park
        time = game.game_state.time
        dave = self.dave

        if time.day < 8:
            pass
        elif time.day < 15:
            dave.progression = 1
        elif time.day < 20:
            dave.progression = 2
        elif time.day < 25:
            dave.progression = 3
        else:
            dave.progression = 4

        if dave.progression < 4:
            if time.weekday() > 4:
                if time.hour > 9 and time.hour < 19:
                    dave.move(park)
                else:
                    dave.move(self)
            elif time.hour < 6:
                dave.move(self)
            elif time.hour < 8:
                dave.move(clss)
            elif time.hour < 15:
                dave.move(self)
            elif time.hour < 16:
                dave.move(clss)
            elif dave.hang_out_day == time.replace(hour=0,minute=0,second=0) and time.hour < 19:
                dave.move(park)
            else:
                dave.move(self)
        else:
            dave.move(self)

dave_void = Davoid()