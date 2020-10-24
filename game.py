import datetime

game_state = None

def game_init(starting_location):
    global game_state
    game_state = GameState(starting_location)

class GameState:
    def __init__(self, location):
        self.location = location
        self.actions = []
        self.time = datetime.datetime(2864, 8, 6, 8, 0, 0)
        self.highlighted_action = 0
        self.active_messages = []
        self.pending_messages = []
        self.refresh()

    def refresh(self):
        self.actions = self.location.get_actions()
        self.highlighted_action = 0
        self.active_messages = self.pending_messages
        self.pending_messages = []

    def execute_action(self, number):
        timecost = self.actions[number].execute()
        self.time += timecost
        self.refresh()

    def input_enter(self):
        self.execute_action(self.highlighted_action)

    def input_up(self):
        self.arrow_change(-1)

    def input_down(self):
        self.arrow_change(1)

    def arrow_change(self, change):
        self.highlighted_action = (self.highlighted_action + change) % len(self.actions)

    def show_message(self, message):
        self.pending_messages.append(message)


'''class WindowState:
    def __init__(self, window):
        self.window = window

    def show_state(self, game_state):
        raise NotImplemented'''


class Object:
    def __init__(self, name, location=None):
        self.name = name
        self.location = location
        self.actions = []
        if location is not None:
            location.add_object(self)
        '''for key in self.__dict__:
            if isinstance(self.__dict__[key], Action):
                self.actions.append(self.__dict__[key])'''

    def get_actions(self):
        return self.actions

    #decorator
    def action(self, name=None, time_cost=datetime.timedelta(0, 0, 0, 0, 1)):
        def decorator(f):
            if isinstance(f, Action):
                raise TypeError("Callback is already an action")
            targetname = name if name else f.__name__
            a = Action(targetname, f, time_cost)
            self.actions.append(a)
            return a

        return decorator


class NPC(Object):
    def __init__(self, name, location=None, friendliness=50):
        self.name = name
        self.friendliness = friendliness
        super().__init__(name, location)


class Location:
    def __init__(self, name=None, neighbors=None):
        self.name = self.__class__.__name__ if name is None else name
        self.neighbors = neighbors
        if neighbors == None:
            self.neighbors = set()
        self.objects = []
        self.location_actions = []

    def when_entering(self):  # To be overriden if needed
        pass

    def when_leaving(self, target_location):  # to be overriden if needed
        if target_location in self.neighbors:
            game_state.location = target_location

    def add_object(self, object):
        self.objects.append(object)

    def add_neighbor(self, neighbor, onedirectional=False, timecost=None):
        self.neighbors.add(neighbor)
        timecost = timecost if timecost else datetime.timedelta(minutes=5)

        @self.location_action(name="Travel to " + neighbor.name ,time_cost=timecost)
        def travel():
            self.when_leaving(neighbor)
            neighbor.when_entering()

        if not onedirectional:
            neighbor.add_neighbor(self, onedirectional=True)

    def get_actions(self):
        ac = []
        for obj in self.objects:
            for action in obj.get_actions():
                ac.append(action)
        for local_action in self.location_actions:
            ac.append(local_action)
        return ac

    #decorator
    def location_action(self, name=None, time_cost=datetime.timedelta(0, 0, 0, 0, 1)):
        def decorator(f):
            if isinstance(f, Action):
                raise TypeError("Callback is already an action")
            targetname = name if name else f.__name__
            a = Action(targetname, f, time_cost)
            self.location_actions.append(a)
            return a

        return decorator


class Action:
    def __init__(self, name, callback, time_cost):
        self.name = name
        self.timecost = time_cost
        self.callback = callback

    def __str__(self):
        return "{0} - {1}".format(self.name, str(self.timecost))

    def execute(self):
        self.callback()
        return self.timecost


#decorators

def object(name=None, location=None):
    def decorator(f):
        if isinstance(f, Object):
            raise TypeError("Func is already Object")
        tergetname = f.__name__ if not name else name
        return Object(tergetname, location)
    return decorator