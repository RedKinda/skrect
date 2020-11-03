import game
import datetime
import redacted.misc_utilities as utils

def dream():
    blue_dream()

def blue_dream():
    willpower = game.game_state.get_stat('willpower')
    needed = 0.6
    game.show_message(str(willpower))

    game.show_message('You are in a strange place. There are trees all around you. One of the trees reminds you of something. Its shape... Or is it the color? It\'s red. Everything is red. Unsurprisingly.')

    dream = game.Dialogue('???', closable=False)
    startdream = dream.start()

    def allow_wakeup():
        @dream.situation('Wake up', response='You suddenly hear ringing. It sounds like... your alarm clock? Oh. It is your alarm clock.', closable=False)
        def wakeup():
            dream.exit()

    allow_wakeup()

    @startdream.situation('Walk towards the tree', response='You walk towards the tree. You have seen it before. Suddenly you remember what it is. It is the tree that stands on Amaryllis street. You are right. You are standing in the middle of the street.', closable=False)
    def tree():
        allow_wakeup()
        if willpower < 1/6*needed: return

        @tree.situation('Hurry to class', response='You look at your watch. The time is 19:25. You are late for class. You sprint through the door to find that everyone is staring at you. Why did you come late again? You do not answer. The teacher is angry with you.', closable=False)
        def classroom():
            allow_wakeup()
            if willpower < 2/6*needed: return

            @classroom.situation('Confront the teacher', response='The teacher takes you to the... The... What is this room? It looks vaguely like an airlock. You are certain there is no airlock in your school. You remember clearly you hid the airlock in your wardrobe last week.', closable=False)
            def airlock():
                allow_wakeup()
                if willpower < 3/6*needed: return

                @airlock.situation('Open the airlock', response='You pull an airkey out of your wardrobe. You unlock the airlock and the airkey dissolves in the air. You look in the airlock and find a small rock. It glows a color you have never seen before. Or have you? You place it in your mouth. It will be safe there.', closable=False)
                def rock():
                    allow_wakeup()
                    if willpower < 4/6*needed: return

                    @rock.situation('Leave the airlock', response='You start walking towards the airlock door. There comes a silent "click" from behind you. As you turn around, you see that your teacher opened the window. Water is flowing into the room. Your hands fill with water. The peculiar rock is no longer in your hand.', closable=False)
                    def water():
                        allow_wakeup()
                        if willpower < 5/6*needed: return

                        @water.situation('Swim through the window', response='You begin to swim. The window is far away. It will take at least an hour to get there. A few seconds later you pass the window frame. As soon as you are out of the room, you fall to the ground. Your glasses break. The rock is in your hand. Its glow blinds you through the cracks in your glasses.', closable=False)
                        def glasses():
                            allow_wakeup()
                            if willpower < 6/6*needed: return

                            @glasses.situation('Take off your glasses', response='You take your glasses off. Everything changes colors. No longer is everything red. You are not supposed to see this. You know you are not. Will you be able to forget this again? There is no going back now. You look at the rock. It hurts to look at it. You hear ringing. It is your alarm clock.', closable=False)
                            def unmasked():
                                game.game_state.glasses.type = game.Alignment.INDEPENDENT
                                game.game_state.set_stat('truth', True)
                                dream.exit()
