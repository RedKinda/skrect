import game
import datetime
import redacted.misc_utilities
from redacted.streets.mainroad import Street

class LongRoad(Street):
    def __init__(self, name='Long road'):
        super().__init__(name=name)

class CrescentLane(Street):
    def __init__(self, name='Crescent lane'):
        super().__init__(name=name)

class LittlewoodRoute(Street):
    def __init__(self, name='Littlewood route'):
        super().__init__(name=name)

# -------------------------------------------

long_road_west = LongRoad('Long road (west)')
long_road_east = LongRoad('Long road (east)')
long_road_west.add_neighbor(long_road_east, timecost=datetime.timedelta(minutes=3))

crescent_lane = CrescentLane()
crescent_lane.add_neighbor(long_road_west, timecost=datetime.timedelta(minutes=2))

littlewood_route = LittlewoodRoute()
