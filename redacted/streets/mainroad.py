import game
import datetime
import redacted.misc_utilities
import random
from redacted.void import void

class Street(game.Location):
    def __init__(self, name):
        super().__init__(name=name)

        @self.action(name="Generate an event here")
        def generate():
            self.sleep_reset()

        @game.object(name="meme", location=self)
        def meme():
            pass

        self.encounter_meme = self.get_object("meme")
        self.encounter_meme.infected = 0
        
        @meme.action(name="Examine note", time_cost=datetime.timedelta(minutes=1), description="A crumpled piece of paper catches your attention.")
        def exameme():
            game.game_state.show_message("The note reads: According to all known laws of aviation, there is no way a bee should be able to fly. It's wings are too small to lift it's fat body off the ground and some more false reasons.")
            if self.encounter_meme.infected == 0:
                self.encounter_meme.infected = 1
                #infection increases slightly
                game.game_state.show_message("INFECTION ++")
            
            inspect_meme = game.Dialogue("A crumpled note.")
            startsit = inspect_meme.start()
            
            @startsit.situation("Try to forget it", response = "It was probably nothing. The Government warned against reading notes lying on the ground anyway.")
            def meme_forget():
                #nothing happens
                pass

            @startsit.situation("Think about it", response = "It makes no sense at all. Not in the slightest. Yet... You feel something moved in your very being.")
            def meme_think():
                if self.encounter_meme.infected == 1:
                    #infection increases slightly
                    game.game_state.show_message("INFECTION ++")
                    self.encounter_meme.infected = 2

            @startsit.situation("Destroy it", response = "You ripped the note apart and threw it away. You feel safer.")
            def meme_destroy():
                #infection decreases slightly
                game.game_state.show_message("INFECTION --")
                self.encounter_meme.move(void)
                

    def sleep_reset(self):
        events = ("none",)*5+("meme",)+("maybe",)*4
        event = random.choice(events)
        self.encounter_meme.move(void)
        if event == "meme":
            self.encounter_meme.move(self)

class MainRoad(Street):
    def __init__(self, name='Main road'):
        super().__init__(name=name)

# -------------------------------------------

main_road_north = MainRoad('Main road (north)')
main_road_south = MainRoad('Main road (south)')
main_road_north.add_neighbor(main_road_south, timecost=datetime.timedelta(minutes=5))

import redacted.streets.littlewood as littlewood
main_road_north.add_neighbor(littlewood.long_road_east, timecost=datetime.timedelta(minutes=3))
main_road_north.add_neighbor(littlewood.littlewood_route, timecost=datetime.timedelta(minutes=2))

import redacted.streets.greatwood as greatwood
main_road_north.add_neighbor(greatwood.hibiscus_street, timecost=datetime.timedelta(minutes=5))
main_road_north.add_neighbor(greatwood.peony_street, timecost=datetime.timedelta(minutes=4))
main_road_north.add_neighbor(greatwood.begonia_street, timecost=datetime.timedelta(minutes=2))
main_road_north.add_neighbor(greatwood.lycoris_street, timecost=datetime.timedelta(minutes=2))
main_road_north.add_neighbor(greatwood.camellia_street, timecost=datetime.timedelta(minutes=4))
main_road_north.add_neighbor(greatwood.poppy_street, timecost=datetime.timedelta(minutes=4, seconds=30))

main_road_south.add_neighbor(greatwood.greatwood_row, timecost=datetime.timedelta(minutes=2, seconds=30))

def run():
    def callback():
        pass

    game.game_init(littlewood.crescent_lane, callback)

    from redacted.school import visit_init
    redacted.school.visit_init()
