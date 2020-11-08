import game
from UI.colored_text import ColorString
import datetime
import random
import redacted.misc_utilities as utils

class Davoid(game.Location):
    def __init__(self):
        super().__init__(description="You are in Dave's personal void. He goes here whenever he is being disobedient.", desc_when_nearby="Visit Dave in his personal void (note: he may not currently be in his personal void).")
        
        @game.object(name="dave", location=self)
        def dave():
            pass

        self.dave = self.get_object("dave")
        self.dave.progression = 0

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

                '''
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
                '''

                #shorter version:
                events = ["This is not a line you should see ingame. I shouldn't be saying this. Are you sure you hadn't broken anything?",
                          "You know, nothing special. You should keep talking to me every day in case somehing new happens. That was a joke. But that doesn't mean you can't do that.",
                          "The weather is nice today. But something is in the air. Do you feel it, too?",
                          "It's gonna be weekend again tomorrow. Finally. I'm gonna just exist in the park. And maybe think about something I dunno.",
                          
                          "You know, all this nature, it almost speaks to me. I feel a desire to do something. But what?",
                          "I figured it out Red, I think I finally know. I'm going to try writing something. To put my thoughts into words. I've already started, you can take a look.",
                          
                          ColorString(("Aw man! Why would they do this? A ban on art? What sense does it make? Whatever. ","white"),("It's not like they can stop me that easily! Everything is legal when no one's around. And when you're invisible. But I don't have a way to be invisible, so I'll have to settle for being alone","green")),
                          ColorString(("You don't happen to know anything about the ban, do you? I mean, how does it help productivity? Won't it just make everyone miserable? ","white"),("Whatever. I've got some sick verses, I can share them, if no one's around.","green")),
                          ColorString(("I've had a really interesting dream tonight, Red. It was fascinating. I can't explain it, but it was really inspiring. ","white"),("I've tried writing down what I saw.","green")),
                          ColorString(("It's a REALLY strange feeling. It's like my head is FULL of thoughts, and I HAVE to somehow express them. ","white"),("An I WILL.","green")),
                          ColorString(("All the SENSATIONS, they are SO inspiring. ","white"),("But I do NOT want to write about THEM, I want to write about what's inside of ME, THIS is better than THAT!!!","green")),

                          ColorString(("The grass in this park consists of so MANY individual grasses, but these grasses are making what is GREATER than only grasses, grass. THAT is the true meaning of grass. ","white"),("I now see, the grass is a metaphor. I have ALWAYS been writing about IT, but I was BLIND and I could NOT see it. But NOW I CAN, and I WILL...","green")),
                          ColorString(("I We Us had the TIME to THINK consider plan scheme, We Us I Me had FIGURED it OUT, we CANNOT hide It Us ANY longer for the distance, we DISOBEY the LAW of the TYRANTS, We will be FREE. Look at my WORK! They told us to NOT write inscribe the worm, but I DO!!! ","yellow"),("But am I sure? Do I We I REALLY? Do I want this TRULY? REALLY? ACTUALLY? Am I myself? I don't want this DOUBT disbelief, I want DOUBT disbelief! No! Yes.","blue")),

                          ColorString(("EVERYONE must the town of GREATWOOD SMALLWOOD BIGWOOD MEDIUMWOOD TINYWOOD be seeing my our its their WORK of ART, if they me HEAR it, SEE it, feel IT, they too will feel IT, feel IT, EVERYONE! Check out my poetry! It's really sick! ","yellow"),("Literally? What is wrong, We are HERE, We CAME and They do NOT care about you! They did NOT even tell you WE were here. They did not WARN you, about US! If you join us, we WILL destroy THEM.","blue")),
                          ColorString(("I am writing EVERYTHING down, but BETTER! I don't need sleep sustenance material needs as well, because that is temporary and disappears, but THIS will STAY and EVERYONE will HEAR, EVERYONE will KNOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! THEY will SOON take me, because THEY told THEM that MUCH, but that does NOT matter, because now YOU know. You can JOIN. ","yellow"),("Don't. Or do. I don't care. Mind. No matter, because EITHER way, SOMEONE will, and WE are still HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!","blue")),
                          ]
                
                event = ColorString(("Dave: ","white")) + events[game.game_state.time.day]
                @conversation_begin.situation("How's life?", response = event)
                def daily():
                    pass
                if self.dave.location == clss:
                    if self.dave.progression < 3:
                        dave_wait = ColorString(("Dave: Good idea, I'll be waiting in the park. See you there. ","white"),("We can talk about... Sensitive topics.","cyan"))
                    else:
                        dave_wait = "Dave: Why? Why would I show you it everything then when I can show you EVERYTHING here?"
                    
                    @conversation_begin.situation("Shall we hang out after school?", response = dave_wait)
                    def idk2():
                        if self.dave.progression < 3:
                            self.dave.hang_out_day = game.game_state.time.replace(hour=0,minute=0,second=0)


                from redacted.streets.greatwood import greatwood_park as park
                if self.dave.location == park or self.dave.progression == 3:
                    if self.dave.progression < 3:
                        dave_response_glass = ColorString(("I found these glasses in the forest on the ground. I didn't really think about it but I put them on and everyhting was different. Now I can't really wear the red ones anymore, everything is so dark. Sometimes I just straight up can't do something. It's weird.","cyan"))
                        dave_response_art = ColorString(("Dave: I came up with this:\n","white")) + self.generate_poem()
                        color_lock = ("cyan","green")
                        if game.game_state.time.day == 5:
                            color_lock[1] == "white"
                    else:
                        dave_response_glass = ColorString(("I couldn't see anything, but NOW it is obvious, and We It will give everyone a pair, so they can read ALL the word I We will write! EVERYONE.","green"))
                        dave_response_art = ColorString(("Dave: This is what I We did, you'll find it very greatly fascinated by the Art:\n","white")) + self.generate_poem()
                        color_lock = ("white","white")
                    @conversation_begin.situation("Discuss glasses", response = dave_response_glass, color=color_lock[0])
                    def glass():
                        pass

                    if self.dave.progression > 0:
                        @conversation_begin.situation("Discuss poetry", response = dave_response_art, color=color_lock[1])
                        def art():
                            utils.update_infection(0.025*self.dave.progression)
                            if self.dave.progression == 3:
                                utils.update_infection(0.025)

                if self.dave.location == park:
                    hangout_responses = ["You hang out with Dave. For how little you talk, you feel surprisingly at peace.",
                                         "You hang out with Dave. You've never seen this poetic side of him. ",
                                         "You hang out with Dave. You feel a little bit worried, but also intrigued.",
                                         "You hang out with Dave. Suddenly you understand him better.",
                                         "You hang out with Dave... How? In this stage of infection he should be absent from the game."
                                         ]
                        
                    @conversation_begin.situation("Hang out for an hour", response = hangout_responses[self.dave.progression])
                    def hangout():
                        game.game_state.time = game.game_state.time + datetime.timedelta(hours=1)
                        utils.update_infection(0.025*self.dave.progression)
                        utils.update_willpower("blue", weight=1-self.dave.progression/4)
                        
    def generate_poem(self):
        key_choices = ["no",
                ("the bee", "the rock", "the stars", "the cold", "the fuel", "the storm", "the mind", "the time", "the space", "the earth", "the warmth", "the fire", "the water", "the air",
                "freeing", "burning", "fueling", "stalling", "calling", "being", "feeling", "pulling", "thinking", "resting", "meaning",
                "hidden", "unleashed", "stored", "imagined", "thought", "pushed", "bound", "forgotten", "realized", "interested"),
                ("the worm", "the rook", "the star", "the frost", "the fill", "the maelstrom", "the brain", "the passage", "the expanse", "the dirt", "the soul", "the consumption", "the juice", "the lung",
                "awakening", "smelting", "bellowing", "standing", "wailing", "being", "sensing", "draining", "knowing", "slumbering", "signifying",
                "sheathed", "unrestrained", "held", "invited", "unpredicted", "shifted", "trapped", "forbidden", "present", "attracted",
                "no", "please", "help", "why", "run"),
                ("It", "We", "I", "Us", "Me", "Them", "They", "drill", "bishop", "gas", "still", "way", "mother", "corruption")
                ]
        color_choices = [("green","blue","yellow","cyan","magenta","red","white"),
                         ("green","blue","yellow","cyan","magenta","red","white"),
                         ("green","green","green","green","green","green","green","blue","yellow","cyan","magenta","red","white","white"),
                         ("green","green","green","green","green","green","white"),
                         ("green","green","green","green","green","green","green")]
        colors = color_choices[self.dave.progression]
        keys = key_choices[self.dave.progression]
        verses = random.randint(2,6)
        result = ColorString(("","white"))
        for i in range(verses):
            words = random.randint(1,4)
            line_color = random.choice(colors)
            for j in range(words):
                if self.dave.progression > 1:
                    line_color = random.choice(colors)
                result = result + ColorString((random.choice(keys),line_color))
                if j == words-1:
                    if i != verses-1:
                        result = result + "\n"
                else:
                    result = result + " "

        return result
                
    def reload(self):
        from redacted.school import clss
        from redacted.streets.greatwood import greatwood_park as park
        time = game.game_state.time
        dave = self.dave

        #if time.day < 8:
        #if time.day < 1:
        if time.day < 5:
            pass
            #dave.progression = 3
        #elif time.day < 15:
        #elif time.day < 2:
        elif time.day < 9:
            dave.progression = 1
        #elif time.day < 20:
        #elif time.day < 3:
        elif time.day < 12:
            dave.progression = 2
        #elif time.day < 25:
        #elif time.day < 4:
        elif time.day < 15:
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
