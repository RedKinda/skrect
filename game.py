import datetime

game_state = None

def game_init(starting_location, callback):
    global game_state
    game_state = GameState(starting_location)
    callback()
    game_state.refresh()


class Alignment:
    GOVERNMENT = "red"
    NEUTRAL = "white"
    INDEPENDENT = "blue"
    HIVEMIND = "green"


class Glasses:
    def __init__(self):
        self.type = Alignment.GOVERNMENT

    def is_action_visible(self, action):
        if self.type == Alignment.GOVERNMENT:
            if action.alignment in [Alignment.GOVERNMENT, Alignment.NEUTRAL]:
                return True
            return False
        else:
            return True

class Interactable:
    def __init__(self):
        self._actions = set()

    # decorator
    def action(self, name=None, **kwargs):
        '''
        Create an action
        :param name: Name
        Optonal arguments:
        :param enabled: Is the action enabled
        :param visible: Is it visible
        :param alignment: Alignment, so it is filtered by glasses
        :param description: Description of this action
        :return:
        '''
        def decorator(f):
            if isinstance(f, Action):
                raise TypeError("Callback is already an action")
            targetname = name if name else f.__name__
            a = Action(targetname, f, **kwargs)
            self._actions.add(a)
            return a
        return decorator

    def get_action(self, name):
        for action in self._actions:
            if action.name == name:
                return action
        return None

    def get_actions(self):
        return self._actions

    def remove_action(self, action):
        if isinstance(action, Action):
            if action in self._actions:
                self._actions.remove(action)
        elif isinstance(action, str):
            for ac in self._actions:
                if ac.name == action:
                    self._actions.remove(ac)
        else:
            raise TypeError("Must be Action or the name of an action as a string")




class GameState(Interactable):
    def __init__(self, location):
        super().__init__()
        self.location = location
        self.visible_actions = []
        self.time = datetime.datetime(2864, 8, 6, 8, 0, 0)
        self.highlighted_action = 0
        self.active_messages = []
        self.pending_messages = []
        self.glasses = Glasses()

    def refresh(self):
        self.visible_actions = self.location.get_actions()
        for ac in self.get_actions():
            if ac.enabled:
                self.visible_actions.append(ac)
        ind = 0
        while ind < len(self.visible_actions):
            if not self.glasses.is_action_visible(self.visible_actions[ind]):
                self.visible_actions.pop(ind)
            else:
                ind += 1
        self.highlighted_action = 0
        self.active_messages = self.pending_messages
        self.pending_messages = []

    def execute_action(self, number: int):
        timecost = self.visible_actions[number].execute()
        self.time += timecost
        self.refresh()

    def execute_action_by_string(self, input_string):
        executed = False
        for action in range(len(self.visible_actions)):
            if self.visible_actions[action].enabled:
                if self.visible_actions[action].name.lower() == input_string:
                    self.execute_action(action)
                    executed = True
                    break
        return executed

    def input_enter(self):
        self.execute_action(self.highlighted_action)

    def input_up(self):
        self.arrow_change(-1)

    def input_down(self):
        self.arrow_change(1)

    def arrow_change(self, change):
        self.highlighted_action = (self.highlighted_action + change) % len(self.visible_actions)

    def show_message(self, message):
        self.pending_messages.append(message)


class Object(Interactable):
    def __init__(self, name, location=None):
        super().__init__()
        self.name = name
        self.location = location
        if location is not None:
            location.add_object(self)
        '''for key in self.__dict__:
            if isinstance(self.__dict__[key], Action):
                self.actions.append(self.__dict__[key])'''


class NPC(Object):
    def __init__(self, name, location=None, friendliness=50):
        self.name = name
        self.friendliness = friendliness
        super().__init__(name, location)


class Location(Interactable):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = kwargs.get("name", self.__class__.__name__)
        self.description = kwargs.get("description", "You are in " + self.name)
        self.desc_when_nearby = kwargs.get("desc_when_nearby", None)
        self.neighbors = set()
        self.objects = []

    def when_entering(self, from_location):
        '''
        This is called when entering this location. If overriden, it should include `game_state.location = self` to move
        :param from_location: Location you are entering from
        :return:
        '''
        game_state.location = self

    def when_leaving(self, target_location):  # to be overriden if needed
        pass

    def add_object(self, object):
        self.objects.append(object)

    def add_neighbor(self, neighbor, onedirectional=False, timecost=None, alignment=Alignment.NEUTRAL):
        self.neighbors.add(neighbor)
        timecost = timecost if timecost else datetime.timedelta(minutes=5)

        @self.action(name="Travel to " + neighbor.name, time_cost=timecost,
                     alignment=alignment, description=neighbor.desc_when_nearby)
        def travel():
            self.when_leaving(neighbor)
            neighbor.when_entering(self)

        if not onedirectional:
            neighbor.add_neighbor(self, onedirectional=True, timecost=timecost, alignment=alignment)

    def get_actions(self):
        ac = []
        for obj in self.objects:
            for action in obj.get_actions():
                ac.append(action)
        for local_action in self._actions:
            ac.append(local_action)
        return ac


class Action:
    def __init__(self, name, callback, **kwargs):
        self.name = name
        self.timecost = kwargs.get("time_cost", datetime.timedelta(minutes=1))
        self.callback = callback
        self.enabled = not kwargs.get("disabled", False)
        self.visible = kwargs.get("visible", True)
        self.alignment = kwargs.get("alignment", Alignment.NEUTRAL)
        self.description = kwargs.get("description", None)

    def __str__(self):
        s = "{0} - {1}".format(self.name, str(self.timecost))
        if self.description is not None:
            s += " - {0}".format(self.description)
        return s

    def print(self):
        if self.enabled and self.visible:
            return str(self)

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