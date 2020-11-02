import game
import datetime
import redacted.misc_utilities
import random
from redacted.void import void

class Street(game.Location):
    def __init__(self, name):
        super().__init__(name=name)

        #@self.action(name="Generate an event here", priority = 6)
        #def generate():
        #    self.sleep_reset()

        @game.object(name="meme", location=self)
        def meme():
            pass

        self.encounter_meme = self.get_object("meme")
        self.encounter_meme.move(void)

        @meme.action(name="Examine note", time_cost=datetime.timedelta(minutes=1), description="A crumpled piece of paper catches your attention.", priority = 5)
        def exameme():
            game.game_state.show_message("The note reads: " + self.encounter_meme.contents)
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

    def meme_randomize(self):
        return random.choice(("Bee", "ä", "The note reads:", "This is a lie", "Get stick bugged lol"))

    def sleep_reset(self):
        events = ("none",)*5+("meme",)+("maybe",)*4
        event = random.choice(events)
        self.encounter_meme.move(void)
        if event == "meme":
            self.encounter_meme.infected = 0
            self.encounter_meme.move(self)
            self.encounter_meme.contents = self.meme_randomize()

class MainRoad(Street):
    def __init__(self, name='Main road'):
        super().__init__(name=name)

# -------------------------------------------

encounter_streets = []

main_road_north = MainRoad('Main road (north)')
main_road_south = MainRoad('Main road (south)')
main_road_north.add_neighbor(main_road_south, timecost=datetime.timedelta(minutes=5))
main_road_north.get_action("Travel to Main road (south)").priority = 10
main_road_south.get_action("Travel to Main road (north)").priority = 10

encounter_streets.append(main_road_north)
encounter_streets.append(main_road_south)

import redacted.streets.littlewood as littlewood
main_road_north.add_neighbor(littlewood.long_road_east, timecost=datetime.timedelta(minutes=3))
main_road_north.add_neighbor(littlewood.littlewood_route, timecost=datetime.timedelta(minutes=2))
main_road_north.get_action("Travel to Long road (east)").priority = 15
littlewood.littlewood_route.get_action("Travel to Main road (north)").priority = 10

encounter_streets.append(littlewood.long_road_east)
encounter_streets.append(littlewood.long_road_west)
encounter_streets.append(littlewood.littlewood_route)
encounter_streets.append(littlewood.crescent_lane)

import redacted.streets.greatwood as greatwood
main_road_north.add_neighbor(greatwood.hibiscus_street, timecost=datetime.timedelta(minutes=5))
main_road_north.add_neighbor(greatwood.peony_street, timecost=datetime.timedelta(minutes=4))
main_road_north.add_neighbor(greatwood.begonia_street, timecost=datetime.timedelta(minutes=2))
main_road_north.add_neighbor(greatwood.lycoris_street, timecost=datetime.timedelta(minutes=2))
main_road_north.add_neighbor(greatwood.camellia_street, timecost=datetime.timedelta(minutes=4))
main_road_north.add_neighbor(greatwood.poppy_street, timecost=datetime.timedelta(minutes=4, seconds=30))

main_road_south.add_neighbor(greatwood.greatwood_row, timecost=datetime.timedelta(minutes=2, seconds=30))

greatwood.hibiscus_street.get_action("Travel to Main road (north)").priority = 10
greatwood.peony_street.get_action("Travel to Main road (north)").priority = 10
greatwood.begonia_street.get_action("Travel to Main road (north)").priority = 10
greatwood.lycoris_street.get_action("Travel to Main road (north)").priority = 10
greatwood.camellia_street.get_action("Travel to Main road (north)").priority = 10
greatwood.poppy_street.get_action("Travel to Main road (north)").priority = 10
greatwood.greatwood_row.get_action("Travel to Main road (north)").priority = 10

encounter_streets.append(greatwood.hibiscus_street)
encounter_streets.append(greatwood.peony_street)
encounter_streets.append(greatwood.begonia_street)
encounter_streets.append(greatwood.dahlia_street)
encounter_streets.append(greatwood.lycoris_street)
encounter_streets.append(greatwood.amaryllis_street)
encounter_streets.append(greatwood.camellia_street)
encounter_streets.append(greatwood.poppy_street)
encounter_streets.append(greatwood.greatwood_row)

def run():
    def callback():
        from redacted.misc_utilities import init_stats
        init_stats()

    from redacted.home import bedroom
    game.game_init(bedroom, callback)

    from redacted.school import visit_init
    redacted.school.visit_init()
