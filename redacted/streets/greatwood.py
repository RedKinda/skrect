import game
import datetime
import redacted.misc_utilities
from redacted.streets.mainroad import Street
from redacted.npcs.dave import dave_void

class HibiscusStreet(Street):
    def __init__(self, name='Hibiscus street'):
        super().__init__(name=name, description="You are on Hibiscus street. There is nothing of interest here. Just some houses.")

class PeonyStreet(Street):
    def __init__(self, name='Peony street'):
        super().__init__(name=name, description="You are on Peony street. You can see the back wall of the school.")

class BegoniaStreet(Street):
    def __init__(self, name='Begonia street'):
        super().__init__(name=name, description="You are on Begonia street. Greatwood park connects here.")

class DahliaStreet(Street):
    def __init__(self, name='Dahlia street'):
        super().__init__(name=name, description="You are on Dahlia street. Located between Peony and Amaryllis street, on the east edge of Greatwood.")

class LycorisStreet(Street):
    def __init__(self, name='Lycoris street'):
        super().__init__(name=name, description="This is Lycoris street. The Inconvenience store is here. This street takes an awkward 90-degree turn.")

class AmaryllisStreet(Street):
    def __init__(self, name='Amaryllis street'):
        super().__init__(name=name, description="This is Amaryllis street. The street in front of Greatwood school.")

class CamelliaStreet(Street):
    def __init__(self, name='Camellia street'):
        super().__init__(name=name, description="You are on Camellia street. There is an entrance to Greatwood park here.")

class PoppyStreet(Street):
    def __init__(self, name='Poppy street'):
        super().__init__(name=name, description="This is Poppy street. It connects to Greatwood row on the side opposite to Main road.")

class GreatwoodRow(Street):
    def __init__(self, name='Greatwood row'):
        super().__init__(name=name, description="This is Greatwood row. The street is at an angle to most other streets. There is a train station here.")

class GreatwoodPark(Street):
    def __init__(self, name="Greatwood park"):
        super().__init__(name=name, description="You are in Greatwood park. This is a great place to hang out with friends.")

    def after_action(self, action_executed):
        dave_void.reload()

# -------------------------------------------

hibiscus_street = HibiscusStreet()
peony_street = PeonyStreet()
begonia_street = BegoniaStreet()
dahlia_street = DahliaStreet()
lycoris_street = LycorisStreet()
amaryllis_street = AmaryllisStreet()
camellia_street = CamelliaStreet()
poppy_street = PoppyStreet()

greatwood_row = GreatwoodRow()

greatwood_park = GreatwoodPark()

peony_street.add_neighbor(begonia_street, timecost=datetime.timedelta(minutes=2))
peony_street.add_neighbor(dahlia_street, timecost=datetime.timedelta(minutes=3))
amaryllis_street.add_neighbor(begonia_street, timecost=datetime.timedelta(minutes=3))
amaryllis_street.add_neighbor(dahlia_street, timecost=datetime.timedelta(minutes=1))
camellia_street.add_neighbor(lycoris_street, timecost=datetime.timedelta(minutes=1))
camellia_street.add_neighbor(amaryllis_street, timecost=datetime.timedelta(minutes=4))
camellia_street.add_neighbor(greatwood_row, timecost=datetime.timedelta(minutes=4))
poppy_street.add_neighbor(greatwood_row, timecost=datetime.timedelta(minutes=2))

greatwood_park.add_neighbor(camellia_street, timecost=datetime.timedelta(minutes=1))
greatwood_park.add_neighbor(begonia_street, timecost=datetime.timedelta(minutes=1))

t = camellia_street.get_action("Travel to Greatwood park")
t.priority = 10
t = begonia_street.get_action("Travel to Greatwood park")
t.priority = 10

import redacted.school as school
amaryllis_street.add_neighbor(school.hall, timecost=datetime.timedelta(minutes=1))
t = amaryllis_street.get_action("Travel to Hall")
t.priority = 10
t.name = 'Travel to Greatwood school'

import redacted.shop as shop
lycoris_street.add_neighbor(shop.main_room, timecost=datetime.timedelta(minutes=1))
t = lycoris_street.get_action("Travel to Main room")
t.priority = 10
t.name = 'Travel to Inconvenience store'

import redacted.station as station
greatwood_row.add_neighbor(station.waiting_room, timecost=datetime.timedelta(minutes=1))
t = greatwood_row.get_action("Travel to Waiting room")
t.priority = 10
t.name = 'Travel to Greatwood station'
