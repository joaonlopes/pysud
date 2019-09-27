
"""
Main pysud module.

Contains basic classes such as the game, player character, levels(rooms)...
"""

import pysud_events as ev
import pysud_str
from functools import reduce

class GameEntity():
    """ Inner use abstract class. """

    def __init__(self):
        self.name = None
        self.uid = None
        self.description = None

    def __str__(self):
        return str(self.uid + ' : ' + self.name)

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_description(self):
        return self.description

    def set_description(self, new_description):
        self.description = new_description

    def get_id(self):
        return self.uid

    def set_id(self, new_id):
        self.uid = new_id


class Item(GameEntity):
    """ A game item (player possession, tool, key, weapon, etc) base class.

    A pysud user must inherit from these class to create her own game items.

    Attributes:
        look_me_ev: pysud_events.LookItemEvent reference.
        use_me_ev: pysud_events.UseItemEvent reference.
        score_value: Default game points the player receives from collecting
            this item.
    """

    def __init__(self, item_name, item_description, item_score_value = 1):
        GameEntity.__init__(self)
        self.set_name(item_name)
        self.set_description(item_description)
        self.__look_me_ev = ev.LookItemEvent(self)
        self.__use_me_ev = ev.UseItemEvent(self)
        self.score_value = item_score_value

    def look_item_event(self):
        """ Answers the pysud_events.LookItemEvent associated
        with the receiver. """
        return self.__look_me_ev

    def use_item_event(self):
        """ Answers the pysud_events.UseItemEvent associated
        with the receiver. """
        return self.__use_me_ev

    def use_on(self, game):
        """ Abstract method.
        A pysud user must implement on her own item classes."""
        pass


class PC(GameEntity):
    """ The player character.

    Attributes:
        score: Variable to hold game score (or points)
        items: Collection of Item object instances
        visited_rooms: Collection of Rooms this player has visited
        current_room: Player Character current location
    """

    def __init__(self, name='Player', description=''):
        GameEntity.__init__(self)
        self.set_name(name)
        self.set_description(description)
        self.score = 0
        self.current_room = None
        self.__items = []
        self.visited_rooms = set()

    def increase_score(self, increase_amount):
        """ Increases the receiver score by a given amount. """
        self.score += increase_amount

    def add_item(self, item):
        """ Adds given item to the receiver items collection. """
        self.__items.append(item)

    def get_items(self):
        """ Returns a python tuple containing the receiver items objects. """
        return tuple(self.__items)

    def has_item(self, item):
        """ Answers whether the receiver has the given item or not.

        Returns:
            True if the receiver PC object has the given item,
            False otherwise.
        """
        return item in self.__items

    def remove_item(self, item):
        """ Removes given item from the receiver items collection.

        Args:
            item: Item class object to remove.

        Returns:
            the removed item instance.
        """
        removed_item = self.__items.remove(item)
        return removed_item

    def has_visited_room(self, room):
        """ Answers whether this object has visited the received room or not.

        Args:
            room: A Room class object.

        Returns:
            True if this PC object has visited given room,
            False otherwise
        """
        return room in self.visited_rooms

    def visited_rooms_amount(self):
        """ Answers how many (unique) rooms the receiver has visited. """
        return len(self.visited_rooms)

    def move_to_room(self, room):
        """ Moves this object to given room,
        then adds room to the visited rooms collection.
        """
        self.current_room = room
        self.visited_rooms.add(room)


class Game():
    """
    Module main class.

    The game itself. Holds most of the relevant objects and handles the
    application main loop.

    Attributes:
        run: Used to flag the game as running/not running.
        pc: PC class instance.
        rooms: The game rooms collection.
        global_events: The game global events collection.
        user_defined_variables: Python dictionary to hold user defined
            variables.
        game_mgr: GameManager class object.
        iom: IOManager class object
    """

    def __init__(self, player_name, save_enabled = True, show_room_items = True, show_room_exits = True):
        self.__run = True
        self.pc = PC(player_name)
        self.rooms = []
        self.__global_events = []
        self.__user_defined_variables = dict()
        self.__game_mgr = None
        self.iom = IOManager(self)
        # Setting game level configuration values:
        self.configs = dict()
        self.configs['SAVE_ENABLED'] = save_enabled
        self.configs['SHOW_ROOMS_ITEMS'] = show_room_items
        self.configs['SHOW_ROOMS_EXITS'] = show_room_exits
        # Adding default global events:
        self.__global_events.append(ev.LookRoomEvent())
        self.__global_events.append(ev.ShowScoreEvent())
        self.__global_events.append(ev.QuitGameEvent())
        self.__global_events.append(ev.ShowPlayerInventoryEvent())
        self.__global_events.append(ev.ShowPlayerStatsEvent())
        self.__global_events.append(ev.ShowHelpEvent())
        if self.configs['SAVE_ENABLED']:
            self.__global_events.append(ev.SaveGameEvent())
            self.__global_events.append(ev.LoadGameEvent())

    def add_global_event(self, event):
        """ Adds a given event to the game's global events collection. """
        self.__global_events.append(event)

    def remove_global_event(self, event):
        """ Removes a given event from the game's global events collection. """
        self.__global_events.remove(event)

    def set_user_defined_variable(self, var_key, var_value):
        """ Adds or modifies a value into the user defined variables collection.

        Args:
            var_key: Identifier for var_value (dictionary key)
            var_value: Value to assign.
        """
        self.__user_defined_variables[var_key] = var_value

    def get_user_defined_variable(self, var_key):
        """ Answers a value defined in the user defined variables collection.

        Args:
            var_key: Identifier for var_value (dictionary key)
        Returns:
            a value associated to var_key
        """
        # TODO doc possible exception
        return self.__user_defined_variables[var_key]

    def add_item_to_player(self, item):
        """ Adds given item to player.

        Also creates global events related to such item.

        Args:
            item: a pysud.Item object.
        """
        self.pc.add_item(item)
        self.__global_events.append(item.look_item_event())
        self.__global_events.append(item.use_item_event())

    def remove_item_from_player(self, item):
        """ Removes given item from player.

        Also removes global events related to given item.

        Args:
            item: a pysud.Item object.
        """
        self.__global_events.remove(item.look_item_event())
        self.__global_events.remove(item.use_item_event())
        self.pc.remove_item(item)

    def quit_game(self):
        """ Terminates game execution and display a goodbye message. """
        self.stop_game()
        self.iom.show_exit_message()

    def stop_game(self):
        """ Stops (doesn't terminates) the game execution. """
        self.__run = False

    def resume_game(self):
        """ Resumes game execution. """
        self.__run = True
        self.run_game()

    def run_game(self):
        """ A game's main loop. """
        self.iom.show_current_room()
        while self.__run:
            self.iom.get_new_user_input()
            success = False  # Valid entries flag
            for gl_ev in self.__global_events:
                if gl_ev.check_conditions(self):
                    gl_ev.on_success(self)
                    success = True
            for lo_ev in self.pc.current_room.get_local_events():
                if lo_ev.check_conditions(self):
                    lo_ev.on_success(self)
                    success = True
            if not success:  # Input didn't match any command
                self.iom.show_error_message()
        return self


    def add_rooms(self, rooms_list):
        """ Adds one or more rooms to this game.

        Args:
            rooms_list: A python list/tuple containing the rooms to be added.
        """
        # TODO doc possible exceptions
        for room in rooms_list:
            self.rooms.append(room)

    def get_room_by_id(self, room_id):
        """ Retrieves a room object given its ID.

        Args:
            room_id: Room identifier to search for

        Returns:
            a Room class object whose id equals room_id
            False if no room with the given id was found.
        """
        # TODO use filter
        i = 0
        found = False
        rooms_amount = len(self.rooms)
        while i < rooms_amount and not found:
            found = self.rooms[i].get_id() == room_id
            i += 1
        if found:
            return self.rooms[i-1]
        else:
            return False

    def save_game(self, filename='save.data'):
        """ Persists the current game.

        Handles pysud_events.SaveGameEvent.
        """
        self.__game_mgr.save_game(filename)

    def load_game(self, filename='save.data'):
        """ Loads a previously persisted game.

        Handles pysud_events.LoadGameEvent.
        """
        self.__game_mgr.load_game(filename)

    def clear_game_mgr(self):
        self.__game_mgr = None

    def set_game_mgr(self, game_manager):
        self.__game_mgr = game_manager


class Room(GameEntity):
    """
    A game level or scenario.

    Attributes:
        items: Items found in the room.
        local_events: Room local events collection.
    """

    def __init__(self, room_name='', room_description='', room_id='0'):
        GameEntity.__init__(self)
        self.set_name(room_name)
        self.set_description(room_description)
        self.set_id(room_id)
        self.__local_events = []
        self.__items = []

    def add_local_event(self, event):
        """ Adds given event to receiver.

        Args:
            event: a pysud_events.Event or one of its subclasses.
        """
        self.__local_events.append(event)

    def get_local_events(self):
        """ Returns a tuple containing the receiver local events. """
        return tuple(self.__local_events)

    def remove_local_event(self, event):
        """ Removes given event from the receiver events collection. """
        self.__local_events.remove(event)

    def add_transition(self, commands, destination):
        """ Adds a new transition to the receiver.

        This method uses its arguments to create a new
        pysud_events.TransitionEvent instance.

        Args:
            commands: A list containing one or more strings
            destination: A pysud.Room object
        """
        self.__local_events.append(ev.TransitionEvent(commands, destination))

    def add_item(self, item):
        """ Adds item to the room and creates the pertinent global event
        PickUpItemEvent. """
        self.__items.append(item)
        self.add_local_event(ev.PickUpItemEvent(item))

    def get_items(self):
        """ Returns a tuple containing the room's pysud.Items. """
        return tuple(self.__items)

    def get_transitions(self):
        return tuple(filter(lambda x: isinstance(x,ev.TransitionEvent), self.__local_events))

    def remove_item(self, item):
        """ Removes item from the room items collection.

        Does not eliminates any event that may be associated with item.
        """
        removed_item = self.__items.remove(item)


class IOManager():
    """
    Handles (cli) I/O operations.

    All input/output operations to be done through command line interface
    should be implemented here.

    Attributes:
        last_user_input: contains the last command read from prompt
        game: A reference to a pysud.Game class instance
        msg_dict: A python dictionary containing general messages strings
    """
    def __init__(self, game):
        self.last_user_input = ''
        self.__game = game
        self.msg_dict = pysud_str.MSG_DICT

    def show_player_stats(self):
        """ Prints the player game's exploration's progress. """
        msg = self.msg_dict['PLAYER_STATS_STR'] + ' ' + str(self.__game.pc.visited_rooms_amount()) + '/' + str(len(self.__game.rooms))
        self.show_message(msg)
    def show_current_room(self):
        """ Prints player current room description and items in it (if any) """
        self.show_message(self.__game.pc.current_room.get_description())
        # TODO add game level flag to disable
        self.show_current_room_exits()
        self.show_current_room_items()

    def show_current_room_exits(self):
        for t in self.__game.pc.current_room.get_transitions():
            self.show_message_list([self.msg_dict['ROOM_EXITS_STR_1'], t.destination.get_name(), self.msg_dict['ROOM_EXITS_STR_2'], str(t.commands)])

    def show_current_room_items(self):
        items = self.__game.pc.current_room.get_items()
        for an_item in items:
            self.show_message_list([self.msg_dict['ROOM_ITEMS_STR'], an_item.get_name()])

    def show_message(self, string):
        """ Prints a given string to std out. """
        print(string)

    def show_message_list(self, strings):
        """ Concatenates collection items with spaces prior to printing out. """
        self.show_mesages(map(lambda s: s + ' ', strings))

    def show_error_message(self):
        """ Prints a 'command not found' or similar message. """
        self.show_message(self.msg_dict['INVALID_CMD_TEXT'])

    def show_player_inventory(self):
        """ Prints the player inventory (items collection). """
        self.show_message(self.msg_dict['PLAYER_INVENTORY_STR'])
        for an_item in self.__game.pc.get_items():
            self.show_message(an_item.get_name())

    def show_score(self):
        """ Prints the player current score. """
        self.show_message_list([self.msg_dict['PLAYER_SCORE_STR'], str(self.__game.pc.score)])

    def get_new_user_input(self):
        """ Reads (and returns) a new input from keyboard. """
        self.last_user_input = input(self.msg_dict['PROMPT_TEXT'])
        return self.last_user_input


    def show_welcome_message(self):
        """ Prints the welcome to a new game message. """
        self.show_message(self.msg_dict['GAME_START_TEXT'])

    def show_welcome_back_message(self):
        """ Prints the welcome message after a loaded game. """
        self.show_message(self.msg_dict['GAME_RESUME_TEXT'])

    def show_help(self):
        """ Prints help message. """
        self.show_message(self.msg_dict['HELP_TEXT'])

    def show_exit_message(self):
        """ Prints a goodbye/game over message. """
        self.show_message(self.msg_dict['GAME_END_TEXT'])

    def show_current_room(self):
        """ Prints player current room description and items in it (if any) """
        self.show_message(self.__game.pc.current_room.get_description())
        if self.__game.configs['SHOW_ROOMS_EXITS']:
            self.show_current_room_exits()
        if self.__game.configs['SHOW_ROOMS_ITEMS']:
            self.show_current_room_items()

    def show_current_room_exits(self):
        for t in self.__game.pc.current_room.get_transitions():
            self.show_message_list([self.msg_dict['ROOM_EXITS_STR_1'], t.destination.get_name(), self.msg_dict['ROOM_EXITS_STR_2'], str(t.commands)])

    def show_current_room_items(self):
        items = self.__game.pc.current_room.get_items()
        for an_item in items:
            self.show_message_list([self.msg_dict['ROOM_ITEMS_STR'], an_item.get_name()])

    def show_message(self, string):
        """ Prints a given string to std out. """
        print(string)

    def show_message_list(self, strings):
        """ Concatenates collection items with spaces prior to printing out. """
        self.show_message(reduce(lambda s,t: s + ' ' + t, strings))

    def show_error_message(self):
        """ Prints a 'command not found' or similar message. """
        self.show_message(self.msg_dict['INVALID_CMD_TEXT'])

    def show_player_inventory(self):
        """ Prints the player inventory (items collection). """
        self.show_message(self.msg_dict['PLAYER_INVENTORY_STR'])
        for an_item in self.__game.pc.get_items():
            self.show_message(an_item.get_name())

    def show_score(self):
        """ Prints the player current score. """
        self.show_message_list([self.msg_dict['PLAYER_SCORE_STR'], str(self.__game.pc.score)])

    def get_new_user_input(self):
        """ Reads (and returns) a new input from keyboard. """
        self.last_user_input = input(self.msg_dict['PROMPT_TEXT'])
        return self.last_user_input
