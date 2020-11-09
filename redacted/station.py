import datetime
import game
from UI.colored_text import ColorString
import redacted.misc_utilities as utils

trains = {
    'westward': {
    ColorString(('Enforcer trasport', 'red')): [['5:52', '5:56'], ['13:52', '13:56'], ['21:52', '21:56']],
    ColorString(('Inconvenience supplies', 'yellow')): [[[4, '10:00'], [4, '11:45']]],
    ColorString(('Civilist express services', 'white')): [['9:56', '10:01'], [[0, 4], ['16:08', '16:13']]]
    },
    'eastward': {
    ColorString(('Enforcer trasport', 'red')): [['6:16', '6:20'], ['14:16', '14:20'], ['22:16', '22:20']],
    ColorString(('Civilist express services', 'white')): [['12:17', '12:22'], [[0, 4], ['17:59', '18:04']]]
    }}

l = len('Civilist express services')
board = ColorString(
    ('''### Line purpose ############## Arr ### Dep ##### Weekday ###
| ''', 'white'), ('Enforcer transport', 'red'), ('''        | 05:52 ... 05:56 |             |
|                           | 13:52 ... 13:56 |             |
| ''', 'white'), ('_________________________', 'red'), (''' | 21:52 ... 21:56 |             |
| Civilist express services | 09:56 ... 10:01 |             |
| _________________________ | 16:08 ... 16:13 | Mon <-> Fri |
| ''', 'white'), ('Inconvenience supplies', 'yellow'), ('''    | 10:00 ... 11:45 | Friday      |
#############################################################
^   WESTWARD   ^   WESTWARD   ^   WESTWARD   ^   WESTWARD   ^
v   EASTWARD   v   EASTWARD   v   EASTWARD   v   EASTWARD   v
### Line purpose ############## Arr ### Dep ##### Weekday ###
| ''', 'white'), ('Enforcer transport', 'red'), ('''        | 06:16 ... 06:20 |             |
|                           | 14:16 ... 14:20 |             |
| ''', 'white'), ('_________________________', 'red'), (''' | 22:16 ... 22:20 |             |
| Civilist express services | 12:17 ... 12:22 |             |
|                           | 17:59 ... 18:04 | Mon <-> Fri |
#############################################################''', 'white')
    )

class WaitingRoom(game.Location):
    def __init__(self, name='Waiting room'):
        super().__init__(name=name, description="You are in the station's waiting room. Only authorized people are allowed on the platform.")

        @self.object('Info board')
        def info_board():
            pass

        @info_board.action('Check train times', description='Look at the arrival times listed for various trains', time_cost=datetime.timedelta(minutes=5))
        def check_train_times():
            game.show_message('You look at the listed times for trains. There is a table on the info board.')
            game.show_message(board)

class Platform(game.Location):
    def __init__(self, name='Platform'):
        super().__init__(name=name)

    def when_entering(self, from_location):
        game.show_message('You are not authorized to go to the platform!')

waiting_room = WaitingRoom()
platform = Platform()
waiting_room.add_neighbor(platform, timecost=datetime.timedelta(minutes=1))
