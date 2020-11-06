import game
import datetime
import redacted.misc_utilities
from redacted.streets.mainroad import Street

class HibiscusStreet(Street):
    def __init__(self, name='Hibiscus street'):
        super().__init__(name=name)

class PeonyStreet(Street):
    def __init__(self, name='Peony street'):
        super().__init__(name=name)

class BegoniaStreet(Street):
    def __init__(self, name='Begonia street'):
        super().__init__(name=name)

class DahliaStreet(Street):
    def __init__(self, name='Dahlia street'):
        super().__init__(name=name)

class LycorisStreet(Street):
    def __init__(self, name='Lycoris street'):
        super().__init__(name=name)

class AmaryllisStreet(Street):
    def __init__(self, name='Amaryllis street'):
        super().__init__(name=name)

class CamelliaStreet(Street):
    def __init__(self, name='Camellia street'):
        super().__init__(name=name)

class PoppyStreet(Street):
    def __init__(self, name='Poppy street'):
        super().__init__(name=name)

class GreatwoodRow(Street):
    def __init__(self, name='Greatwood row'):
        super().__init__(name=name)

class GreatwoodPark(Street):
    def __init__(self, name="Greatwood park"):
        super().__init__(name=name)

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
