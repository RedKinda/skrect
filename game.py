import datetime
import collections
import hashlib

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

from UI.colored_text import ColorString
class EnergyCost:
    NONE = 0
    MENTAL = 1
    TRAVEL = 2
    LIGHT = 3
    MEDIUM = 4
    HEAVY = 5


def show_message(message):
    game_state.show_message(message)


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
            if str(action.name) == name:
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
        self.time = datetime.datetime(2120, 5, 1, 7, 0, 0)
        self.highlighted_action = 0
        self.active_messages = []
        self.pending_messages = []
        self.player_stats = {}
        self.post_action_triggers = set()
        self.glasses = Glasses()

    def refresh(self):
        self.possible_actions = self.location.get_actions()
        self.visible_actions = []
        for ac in self.get_actions():
            if ac.enabled and ac.get_infection_treshold() > self.get_stat("infection") * 100:
                self.possible_actions.append(ac)
        ind = 0
        for action in self.possible_actions:
            if (not self.glasses.is_action_visible(action)) or not action.visible or not action.enabled:
                ind += 1
            else:
                self.visible_actions.append(action)
        self.visible_actions.sort(key=lambda action: action.priority)
        self.highlighted_action = 0
        self.active_messages = self.pending_messages
        self.pending_messages = []

    def execute_action_from_list(self, number: int):
        if number >= len(self.visible_actions):
            return False
        self._execute_action(self.possible_actions.index(self.visible_actions[number]))

    def _execute_action(self, number: int, ):
        action = self.possible_actions[number]
        timecost = action.execute()
        self.time += timecost
        self.location.after_action(action)
        for cb in self.post_action_triggers:
            cb(action)
        self.refresh()
        return True

    def execute_action_by_string(self, input_string):
        executed = False
        for action in range(len(self.possible_actions)):
            if self.possible_actions[action].enabled:
                if self.possible_actions[action].name.lower() == input_string:
                    self._execute_action(action)
                    executed = True
                    break
        return executed

    def input_enter(self):
        if len(self.visible_actions):
            self.execute_action_from_list(self.highlighted_action)

    def input_up(self):
        self.arrow_change(-1)

    def input_down(self):
        self.arrow_change(1)

    def arrow_change(self, change):
        if len(self.visible_actions) > 0:
            self.highlighted_action = (self.highlighted_action + change) % len(self.visible_actions)

    def show_message(self, message):
        self.pending_messages.append(message)

    def set_stat(self, name, value):
        self.player_stats[name] = value

    def get_stat(self, name):
        return self.player_stats[name]

    def init_stat(self, name, value):
        if name not in self.player_stats:
            self.set_stat(name, value)
        else:
            raise KeyError

    def add_post_action_trigger(self, callback):
        if not isinstance(callback, collections.Callable):
            raise TypeError("Trigger must be callable")
        self.post_action_triggers.add(callback)


class Glasses:
    def __init__(self):
        self.type = Alignment.GOVERNMENT

    def is_action_visible(self, action):
        if self.type == Alignment.GOVERNMENT:
            if action.alignment in [Alignment.GOVERNMENT, Alignment.NEUTRAL]:
                return True
            return False
        elif self.type == Alignment.INDEPENDENT:
            return True
        elif self.type == Alignment.HIVEMIND:
            if action.alignment in [Alignment.HIVEMIND, Alignment.NEUTRAL]:
                return True
            return False


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

    def move(self, destination):
        if not isinstance(destination, Location):
            raise TypeError("Destination must be location")
        self.location.objects.remove(self)
        destination.objects.append(self)
        self.location = destination


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

    def after_action(self, action_executed):
        '''
        This can be ovverriden as it is called any time an action was executed
        :param action_executed: Action that was executed
        :return:
        '''
        pass

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

        # if travel_text and (not onedirectional): raise ValueError

        if travel_text is None:
            travel_text = "Travel to " + neighbor.name

        @self.action(name=travel_text, time_cost=timecost, alignment=alignment, description=neighbor.desc_when_nearby)
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

    def get_object(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    def object(self, name=None):
        def decorator(f):
            if isinstance(f, Object):
                raise TypeError("Func is already Object")
            tergetname = f.__name__ if not name else name
            return Object(tergetname, self)

        return decorator


class Action:
    color_to_alignment = {
        "red": Alignment.GOVERNMENT,
        "magenta": Alignment.GOVERNMENT,
        "yellow": Alignment.NEUTRAL,
        "white": Alignment.NEUTRAL,
        "green": Alignment.HIVEMIND,
        "cyan": Alignment.HIVEMIND,
        "blue": Alignment.INDEPENDENT
    }

    def __init__(self, name, callback, **kwargs):
        self.timecost = kwargs.get("time_cost", datetime.timedelta(minutes=1))
        self.callback = callback
        self.enabled = not kwargs.get("disabled", False)
        self.visible = kwargs.get("visible", True)
        self.color = kwargs.get("color", "white")
        self.name = ColorString((name, self.color))
        self.alignment = kwargs.get("alignment", self.color_to_alignment[self.color])
        self.description = kwargs.get("description", None)
        self.priority = kwargs.get("priority", 50)
        self.energycost = kwargs.get("energycost", EnergyCost.MENTAL)
        self.last_seed = None
        self.last_hash = None

    def __str__(self):
        s = "{0}".format(self.name)
        if self.timecost != datetime.timedelta(seconds=0):
            s += " - {0}".format(str(self.timecost))
        if self.description is not None:
            s += " - {0}".format(self.description)
        return s

    def get_infection_treshold(self):
        seed = game_state.get_stat("seed")
        if seed == self.last_seed:
            pass
        else:
            self.last_seed = seed
            self.last_hash = int(hashlib.sha1((str(self.name) + str(seed)).encode()).hexdigest(), 16) % 100
        return self.last_hash

    def print(self):
        if self.enabled and self.visible:
            s = self.name
            if self.timecost != datetime.timedelta(seconds=0):
                s += " - " + str(self.timecost)
            if self.description is not None:
                s += ColorString(" - ") + self.description
            return s

    def execute(self):
        self.callback()
        cost = self.energycost * self.timecost.total_seconds()
        #msg = ColorString(("You would lose "), (cost, "yellow"), (" points of energy"))
        #show_message(msg)
        return self.timecost

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True


class Situation(Action):
    def __init__(self, name, callback, dialogue, timecost=datetime.timedelta(seconds=0), **kwargs):
        super().__init__(name, callback, time_cost=timecost, **kwargs)
        self.response = kwargs.get("response", "You are waiting.")
        self.dialogue = dialogue
        self.closable = kwargs.get("closable", "Goodbye!")
        self.subsituations = []
        if self.closable:
            @self.situation(self.closable, closable=False, priority=100, response="")
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
    def __init__(self, description, **kwargs):
        Location.__init__(self, description=description)
        def empty():
            pass
        self.active_situation = Situation(None, empty, self, **kwargs)
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
