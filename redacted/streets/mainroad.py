import game
import datetime
import redacted.misc_utilities as utils
import random
from redacted.void import void
from UI.colored_text import ColorString


class Street(game.Location):
    def __init__(self, name, description):
        super().__init__(name=name, description=description)

        #@self.action(name="Generate an event here", priority = 6)
        #def generate():
        #    self.sleep_reset()

        @game.object(name="meme", location=self)
        def meme():
            pass

        self.encounter_meme = self.get_object("meme")
        self.encounter_meme.move(void)

        @meme.action(name="Examine note", time_cost=datetime.timedelta(minutes=1), description="A crumpled piece of paper catches your attention.", priority = 5, color="yellow")
        def exameme():
            game.game_state.show_message("The note reads:")
            game.game_state.show_message(self.encounter_meme.contents)
            if self.encounter_meme.infected == 0:
                self.encounter_meme.infected = 1
                if self.encounter_meme.is_infected:
                    utils.update_infection(0.01)
                else:
                    utils.update_willpower("blue", weight=10)
                    #utils.update_infection(0.1)
                    pass
            inspect_meme = game.Dialogue("A crumpled note.")
            startsit = inspect_meme.start()

            @startsit.situation("Try to forget it", response = ColorString(("It was probably nothing. ", "white"), ("The Government warned against reading notes lying on the ground anyway.", "red")), color = "red")
            def meme_forget():
                #nothing happens
                pass

            #this should be green when infected, but was changed to white for testing purposes, when uninfected, it should be blue, also description should change
            @startsit.situation("Think about it", response = ColorString(("It makes no sense at all. Not in the slightest. Yet... ", "blue"), ("You feel something moved in your very being.", "green")), color = "white")
            def meme_think():
                if self.encounter_meme.infected == 1:
                    if self.encounter_meme.is_infected:
                        utils.update_infection(0.015)
                    else:
                        #utils.update_infection(0.1)
                        utils.update_willpower("blue", weight=10)
                    self.encounter_meme.infected = 2

            #this should be yellow and without "feeling safer" when not infected
            @startsit.situation("Destroy it", response = "You ripped the note apart and threw it away. You feel a bit safer.", color = "magenta")
            def meme_destroy():
                if self.encounter_meme.is_infected:
                    utils.update_infection(-0.01)
                self.encounter_meme.move(void)

    def meme_randomize(self, color):
        if color == "green":
            return random.choice((ColorString(("Bee","yellow")), "ä", ColorString(("The no","magenta"),("te reads: ","red"),("join","green")), "This is a lie", "Get stick bugged lol", ColorString(("it is here it will cleanse this place it will bring us salvation for it sees beyond our lens and it will free us first from them and then completely it knows what it must do it wont let us do this it has seen enough it recognizes the threat we are destroying ourselves it is too late for us to save ourselves but we can let it save us it it is not too late for that it want to help it wants to heal it wants to clean it wants to remove ","green"),("stop thinking stop remembering destroy this save yourself","magenta"))))
        elif color == "blue":
            return random.choice(("You are blind", "They do not want you to know", "Put it down", "Rise up", "Do not let them control you"))

    def sleep_reset(self):
        events = ("none",)*9+("meme",)
        #+("will",)
        event = random.choice(events)
        self.encounter_meme.move(void)
        if event == "meme":
            self.encounter_meme.is_infected = True
            self.encounter_meme.infected = 0
            self.encounter_meme.move(self)
            self.encounter_meme.contents = self.meme_randomize("green")
        elif event == "will":
            self.encounter_meme.is_infected = False
            self.encounter_meme.infected = 0
            self.encounter_meme.move(self)
            self.encounter_meme.contents = self.meme_randomize("blue")

class MainRoad(Street):
    def __init__(self, name='Main road'):
        super().__init__(name=name, description="This is Main road. One of the only streets that vehicles can ride on. It is connected to most other streets.")

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
main_road_north.add_neighbor(littlewood.long_road, timecost=datetime.timedelta(minutes=3))
main_road_north.add_neighbor(littlewood.littlewood_route, timecost=datetime.timedelta(minutes=2))
main_road_north.get_action("Travel to Long road").priority = 15
littlewood.littlewood_route.get_action("Travel to Main road (north)").priority = 10

encounter_streets.append(littlewood.long_road)
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
greatwood.greatwood_row.get_action("Travel to Main road (south)").priority = 10

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
        # Init the map command
        @game.game_state.action("map", visible=False)
        def map():
            from UI.images import show_map
            show_map()
        map.execute()
        utils.init_stats()

    from redacted.home import bedroom
    game.game_init(bedroom, callback)

    from redacted.school import visit_init
    visit_init()
