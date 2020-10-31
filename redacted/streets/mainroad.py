import game
import datetime
import redacted.misc_utilities

class Street(game.Location):
    def __init__(self, name):
        super().__init__(name=name)

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
