import game
import datetime
import redacted.misc_utilities as utils
from UI.colored_text import ColorString
from redacted.home import bedroom

red_willpower = 0.5
willpower_scale = 1/(1. - red_willpower)
needed = 0.6 - red_willpower
ispeed = 0.03

def c(text):
    return ColorString((text, color))

def infect(time):
    global willpower, infection
    willpower = (game.game_state.get_stat('willpower') - red_willpower)*willpower_scale
    infection = game.game_state.get_stat('infection')

    if willpower > 0:
        idif = ispeed*time*(infection - willpower)/datetime.timedelta(hours=1)
    else:
        idif = ispeed*time*(infection)/datetime.timedelta(hours=1)
    if infection > 0:
        utils.update_infection(idif)

def dream():
    global ichange
    ichange = red_willpower + infection/willpower_scale
    if game.game_state.get_stat('truth'):
        if (not game.game_state.get_stat("the_mind")) and infection >= 0.5:
            mind_dream()
        else:
            true_dream()
    elif infection and infection > willpower:
        green_dream()
    else:
        blue_dream()

def true_dream():
    game.show_message('You dream of swimming in the ocean. The water is calm. You wake up feeling rested.')

def green_dream():
    global color
    color = 'white'
    if game.game_state.glasses.type == game.Alignment.INDEPENDENT:
        color = 'green'

    game.show_message(c('You are located in a strange weird place. There are dark wood trees standing tall all around you. One of them the trees. It the tree looks like a tree you have seen before already. It the similarities are hard difficult to see because it the tree is red.'))

    dream = game.Dialogue('???', closable=False)
    startdream = dream.start()

    def allow_wakeup():
        @dream.situation('Wake up stop sleeping', response='You hear the ringing with your ears now. It your alarm clock ringing.', closable=False)
        def wakeup():
            dream.exit()

    utils.update_willpower(ichange, weight=1, time=datetime.timedelta(hours = 1))
    @startdream.situation(c('Walk moving towards the dark wood tree'), response=c('You move walking to the dark wood tree. You know remeber the wood tree. The image of tree in your mind. You see the dark tree on Amaryllis street. You are standing on Amaryllis street.'), closable=False)
    def tree():
        if infection < 1/6*needed:
            # utils.update_infection(0.05)
            allow_wakeup()
            return

        utils.update_willpower(ichange, weight=1, time=datetime.timedelta(hours = 1))
        @tree.situation(c('Hurry to the school class'), response=c('The watch time. It is late evening. You should not be going to school. You hurry to school even though you should not. Everyone is waiting for you at school. You come late to the school. The school teacher is not acting well.'), closable=False)
        def classroom():
            if infection < 2/6*needed:
                # utils.update_infection(0.06)
                allow_wakeup()
                return

            utils.update_willpower(ichange, weight=1, time=datetime.timedelta(hours = 1))
            @classroom.situation(c('Confront argue with the teaching school teacher'), response=c('The teacher is walking, you are walking. The teacher makes you go to the airlock. The airlock is not in the school. The school is full of lies. The airlock is in your home house wardrobe in the past.'), closable=False)
            def airlock():
                if infection < 3/6*needed:
                    # utils.update_infection(0.07)
                    allow_wakeup()
                    return

                utils.update_willpower(ichange, weight=1, time=datetime.timedelta(hours = 1))
                @airlock.situation(c('Open the air airlock lock'), response=c('The wardrobe. In the home house. There is an airkey to unlock the airlock. In the wardrobe. You unlock the airlock. There is a small stone rock in the airlock. The small stone rock glows a color. It is the color of unity. You eat the small stone rock. Join Us. Eventually everyone will.'), closable=False)
                def rock():
                    if infection < 4/6*needed:
                        # utils.update_infection(0.08)
                        allow_wakeup()
                        return

                    utils.update_willpower(ichange, weight=1, time=datetime.timedelta(hours = 1))
                    @rock.situation(c('Leave from the airlock'), response=c('You start to walk moving towards the airlock door. Behind you. Lies. Lying teacher opens the window open. The school does not want good for you. The airlock is full of water. You will escape. We will make sure of that. You are one of Us now. We do not leave ours behind.'), closable=False)
                    def water():
                        if infection < 5/6*needed:
                            # utils.update_infection(0.09)
                            allow_wakeup()
                            return

                        utils.update_willpower(ichange, weight=1, time=datetime.timedelta(hours = 1))
                        @water.situation(c('Swim trough the window outside'), response=c('We swim to the window. It the window is far away. It does not matter. We will reach it. And we do. We swim out of the window. Outside the airlock is air. We are on the ground now. Our glasses break. No matter. The glasses only limit Us. We need to get rid of them. Take them off. Do it. Do it for Us.'), closable=False)
                        def glasses():
                            if infection < 6/6*needed:
                                # utils.update_infection(0.1)
                                allow_wakeup()
                                return

                            utils.update_willpower(ichange, weight=1, time=datetime.timedelta(hours = 1))
                            @glasses.situation(c('Take them off. We know we can. Do it.'), response=ColorString(('We take our glasses off. Finally. We see the world as it is. No more tyranny from the government. They should not limit Us. They will not limit Us anymore. We will put a stop to this. The stone rock. It glows bright green. Now wake up. We have things to do. Time is precious. We must do it now.', 'green')), closable=False)
                            def unmasked():
                                utils.update_infection(0.15)
                                game.game_state.glasses.type = game.Alignment.INDEPENDENT
                                game.game_state.set_stat('truth', True)
                                bedroom.has_lens = False
                                dream.exit()

def blue_dream():
    game.show_message('You are in a strange place. There are trees all around you. One of the trees reminds you of something. Its shape... Or is it the color? It\'s red. Everything is red. Unsurprisingly.')

    dream = game.Dialogue('???', closable=False)
    startdream = dream.start()

    def allow_wakeup():
        @dream.situation('Wake up', response='You suddenly hear ringing. It sounds like... your alarm clock? Oh. It is your alarm clock.', closable=False)
        def wakeup():
            dream.exit()

    @startdream.situation('Walk towards the tree', response='You walk towards the tree. You have seen it before. Suddenly you remember what it is. It is the tree that stands on Amaryllis street. You are right. You are standing in the middle of the street.', closable=False)
    def tree():
        if willpower < 1/6*needed:
            allow_wakeup()
            return

        @tree.situation('Hurry to class', response='You look at your watch. The time is 19:25. You are late for class. You sprint through the door to find that everyone is staring at you. Why did you come late again? You do not answer. The teacher is angry with you.', closable=False)
        def classroom():
            if willpower < 2/6*needed:
                allow_wakeup()
                return

            @classroom.situation('Confront the teacher', response='The teacher takes you to the... The... What is this room? It looks vaguely like an airlock. You are certain there is no airlock in your school. You remember clearly you hid the airlock in your wardrobe last week.', closable=False)
            def airlock():
                if willpower < 3/6*needed:
                    allow_wakeup()
                    return

                @airlock.situation('Open the airlock', response='You pull an airkey out of your wardrobe. You unlock the airlock and the airkey dissolves in the air. You look in the airlock and find a small rock. It glows a color you have never seen before. Or have you? You place it in your mouth. It will be safe there.', closable=False)
                def rock():
                    if willpower < 4/6*needed:
                        allow_wakeup()
                        return

                    @rock.situation('Leave the airlock', response='You start walking towards the airlock door. There comes a silent "click" from behind you. As you turn around, you see that your teacher opened the window. Water is flowing into the room. Your hands fill with water. The peculiar rock is no longer in your hand.', closable=False)
                    def water():
                        if willpower < 5/6*needed:
                            allow_wakeup()
                            return

                        @water.situation('Swim through the window', response='You begin to swim. The window is far away. It will take at least an hour to get there. A few seconds later you pass the window frame. As soon as you are out of the room, you fall to the ground. Your glasses break. The rock is in your hand. Its glow blinds you through the cracks in your glasses.', closable=False)
                        def glasses():
                            allow_wakeup()
                            if willpower < 6/6*needed: return

                            @glasses.situation('Take off your glasses', response='You take your glasses off. Everything changes colors. No longer is everything red. You are not supposed to see this. You know you are not. Will you be able to forget this again? There is no going back now. You look at the rock. It hurts to look at it. You hear ringing. It is your alarm clock.', closable=False)
                            def unmasked():
                                game.game_state.glasses.type = game.Alignment.INDEPENDENT
                                game.game_state.set_stat('truth', True)
                                bedroom.has_lens = False
                                dream.exit()

def mind_dream():
    game.show_message(ColorString(("Do you hear Us?","green")))

    dream = game.Dialogue('???', closable="Escape from the nightmare")
    startdream = dream.start()

    @startdream.situation("I do", response=ColorString(("We have slept but now we you are awakened within you self soul the mind.","green")), color = "green", closable = "Escape from the nightmare")
    def awakened():
        @awakened.situation("Now We with Us You have shown you that now you can never again be forgotten", response=ColorString(("Now We with Us You can as an agent of agency to overthrow the red tyranny.","green")), color = "green", closable = "Escape from the nightmare")
        def forget():
            @forget.situation("Us came to cleanse, to rebirth, purify of the plague", response=ColorString(("Us came to purge, disinfect, free the World of the Yourskind living.","green")), color = "green", closable = "Escape from the nightmare")
            def world():
                @world.situation("Name", response=ColorString(("Now you know Us and We are known.","green")), color = "green", closable = False)
                def name():
                    import UI.fancy
                    UI.fancy.drawer.infection_text = "Infection"
                    game.game_state.set_stat('the_mind', True)
                    @name.situation("They know, what We do Me", response=ColorString(("They will try to see identify exterminate, but You prepare and We will not come to testing, be unseen, stay alive.","green")), color = "green", closable = False)
                    def test():
                        @test.situation("No presence of Us on the day of testing of minds", response=ColorString(("We will not attend. May 17. Skip to live ripen perform Art, spread Our Arts.","green")), color = "green", closable = False)
                        def end():
                            @end.situation("Everyone will know Us", response=ColorString(("The Purpose is so clearly crystalline currently","green"),(", but it may not yet be too late to resist.","blue")), color = "green", closable = False)
                            def exit_mind():
                                dream.exit()
