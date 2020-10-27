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

def show_message(message):
    game_state.show_message(message)

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
        self.possible_actions = []
        self.time = datetime.datetime(2864, 8, 6, 8, 0, 0)
        self.highlighted_action = 0
        self.active_messages = []
        self.pending_messages = []
        self.glasses = Glasses()

    def refresh(self):
        self.possible_actions = self.location.get_actions()
        self.visible_actions = []
        for ac in self.get_actions():
            if ac.enabled:
                self.possible_actions.append(ac)
        ind = 0
        for action in self.possible_actions:
            if (not self.glasses.is_action_visible(action)) or (not action.visible):
                ind += 1
            else:
                self.visible_actions.append(action)
        self.highlighted_action = 0
        self.active_messages = self.pending_messages
        self.pending_messages = []

    def execute_action_from_list(self, number: int):
        if number >= len(self.visible_actions):
            return False
        self.execute_action(self.possible_actions.index(self.visible_actions[number]))

    def execute_action(self, number: int, ):
        timecost = self.possible_actions[number].execute()
        self.time += timecost
        self.refresh()
        return True

    def execute_action_by_string(self, input_string):
        executed = False
        for action in range(len(self.possible_actions)):
            if self.possible_actions[action].enabled:
                if self.possible_actions[action].name.lower() == input_string:
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

    def add_neighbor(self, neighbor, onedirectional=False, timecost=None, alignment=Alignment.NEUTRAL,
                     travel_text=None):
        self.neighbors.add(neighbor)
        timecost = timecost if timecost else datetime.timedelta(minutes=5)

        if travel_text is None:
            travel_text = "Travel to " + neighbor.name
        @self.action(name=travel_text, time_cost=timecost,
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


class Situation(Action):
    def __init__(self, name, callback, dialogue, timecost=datetime.timedelta(seconds=0), **kwargs):
        super().__init__(name, callback, time_cost=timecost)
        self.response = kwargs.get("response", "You are waiting")
        self.dialogue = dialogue
        self.closable = kwargs.get("closable", True)
        self.subsituations = []
        self.priority = kwargs.get("priority", 50)
        if self.closable:
            @self.situation("Goodbye!", closable=False, priority=100)
            def close():
                self.dialogue.exit()

    def situation(self, name=None, **kwargs):
        def decorator(f):
            if isinstance(f, Situation):
                raise TypeError("This is already a Situation")
            tergetname = f.__name__ if not name else name
            sit = Situation(tergetname, f, self.dialogue, **kwargs)
            self.subsituations.append(sit)
            return sit
        return decorator

    def execute(self):
        timecost = super().execute()
        self.dialogue.update_situation(self)
        return timecost


    def get_actions(self):
        return self.subsituations


class Dialogue(Location):
    def __init__(self, description):
        Location.__init__(self, description=description)
        def empty():
            pass
        self.active_situation = Situation(None, empty, self)
        self.last_location = None
        self.local_situations = []

    def set_starting_situation(self, situation: Situation):
        self.active_situation = situation

    def get_actions(self):
        ac = self.active_situation.get_actions()
        for a in self.local_situations:
            ac.append(a)
        self.local_situations = []
        return ac

    def update_situation(self, situation):
        self.active_situation = situation
        game_state.show_message(situation.response)

    def when_entering(self, from_location):
        game_state.location = self
        self.last_location = from_location

    def start(self):
        self.when_entering(game_state.location)
        return self.active_situation

    def exit(self):
        game_state.location = self.last_location
        #self.last_location.when_entering(self)

    def situation(self, name=None, **kwargs):
        def decorator(f):
            if isinstance(f, Situation):
                raise TypeError("This is already a Situation")
            tergetname = f.__name__ if not name else name
            sit = Situation(tergetname, f, self, **kwargs)
            self.local_situations.append(sit)
            return sit
        return decorator






#decorators

def object(name=None, location=None):
    def decorator(f):
        if isinstance(f, Object):
            raise TypeError("Func is already Object")
        tergetname = f.__name__ if not name else name
        return Object(tergetname, location)
    return decorator