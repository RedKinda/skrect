import game
import datetime
import redacted.misc_utilities
from redacted.streets.mainroad import Street

class LongRoad(Street):
    def __init__(self, name='Long road'):
        super().__init__(name=name, description="This is Long road. It is, indeed, very long. Unsurprisingly.")

class CrescentLane(Street):
    def __init__(self, name='Crescent lane'):
        super().__init__(name=name, description="You are on Crescent lane. The street has a curved shape. Your home is located here.")

class LittlewoodRoute(Street):
    def __init__(self, name='Littlewood route'):
        super().__init__(name=name, description="Littlewood route. Connected to Main road twice. Not that it helps anyone.")

# -------------------------------------------

long_road = LongRoad('Long road')

crescent_lane = CrescentLane()
crescent_lane.add_neighbor(long_road, timecost=datetime.timedelta(minutes=2))

littlewood_route = LittlewoodRoute()

import redacted.home as home
crescent_lane.add_neighbor(home.hall, timecost=datetime.timedelta(minutes=1))

crescent_lane.get_action("Travel to Hallway").priority = 10
crescent_lane.get_action("Travel to Hallway").name = "Travel home"
