
"""
pysud Event hierarchy module

Contains classes to represent different game events, such as using an item,
    player moving to a room, etc.
"""

import pysud_str as ps

class Event():
    """ Base (abstract) Event class. """
    def __init__(self):
        self.uid = None

    def check_conditions(self, game):
        """ Checks if this event occurs.

        Returns:
            True on this event occurring, False otherwise.
        """
        pass

    def on_success(self, game):
        """ This method will be called when the event occurs. """
        pass

class ScoreEvent(Event):
    """ These kind of events occurs when the player's score reaches a
    given value.

    Attributes:
        score_trigger: A (minimal) score ammount.
    """
    def __init__(self, score_number):
        Event.__init__(self)
        self.score_trigger = score_number

    def check_conditions(self, game):
        return game.pc.score >= self.score_trigger

class LocationEvent(Event):
    """ These kinds of events occurs when the player is on one of given
    room/s.

    Attributes:
        rooms: A pysud.Room object list.
     """
    def __init__(self, rooms):
        Event.__init__(self)
        self.rooms = tuple(rooms)

    def check_conditions(self, game):
        """ Checks wether the player is on one of the designated rooms. """
        return game.pc.current_room in self.rooms


class CommandEvent(Event):
    """ Base command Event.

    These kind of events occurs when player inputs certain command(s).

    Attributes:
        commands: Event trigger(s) string(s).
    """

    def __init__(self, commands):
        Event.__init__(self)
        # TODO consider using set or frozenset instead
        self.commands = tuple(commands)

    def check_conditions(self, game):
        """ Checks if this event occurs.

        Returns:
            True on this event occurring, False otherwise.
        """
        return game.iom.last_user_input in self.commands


class TransitionEvent(CommandEvent):
    """ Transition (movement) event.

    Transition events are those that move the player character from one
    room to another.

    Attributes:
        destination: Room object where the player character will be
            transported on this event's success.
    """

    def __init__(self, commands, destination):
        CommandEvent.__init__(self, commands)
        self.destination = destination

    def on_success(self, game):
        game.pc.move_to_room(self.destination)
        game.iom.show_current_room()


class ShowMessageEvent(CommandEvent):
    """ Message Event.

    When this kind of events occurs a message will be shown on screen.

    Attributes:
        message: String containing the message to display.
    """

    def __init__(self, commands, message):
        CommandEvent.__init__(self, commands)
        self.message = message

    def on_success(self, game):
        game.iom.show_message(self.message)


class LookRoomEvent(CommandEvent):
    """ """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_LOOK)

    def on_success(self, game):
        game.iom.show_current_room()


class LookItemEvent(ShowMessageEvent):
    """ """
    def __init__(self, item):
        cmd = ps.simple_map(ps.CMD_LOOK,item.name)
        ShowMessageEvent.__init__(self, commands = cmd, message = item.description)


class PickUpItemEvent(CommandEvent):
    """ """
    def __init__(self, an_item):
        self.item = an_item
        CommandEvent.__init__(self, commands = ps.simple_map(ps.CMD_ITEM_GET,self.item.name))

    def on_success(self, game):
        game.add_item_to_player(self.item)
        game.pc.score += self.item.score_value
        game.iom.show_message_list([ps.MSG_DICT['ITEM_RETRIEVED'],self.item.name])
        game.pc.current_room.remove_local_event(self)
        game.pc.current_room.remove_item(self.item)


class UseItemEvent(CommandEvent):
    """  """
    def __init__(self, an_item):
        self.item = an_item
        CommandEvent.__init__(self, commands = ps.simple_map(ps.CMD_ITEM_USE,self.item.name))

    def on_success(self, game):
        self.item.use_on(game)


class CombineItemEvent(CommandEvent):
    """ These events are useful to combine two different items into a
    new one. """
    def __init__(self, component_item_a, component_item_b, result_item):
        self.__component_item_a = component_item_a
        self.__component_item_b = component_item_b
        cmd = ps.complex_map(ps.CMD_ITEM_COMBINE,self.__component_item_a,self.component_item_b)
        CommandEvent.__init__(self, commands = cmd)
        self.__result_item = result_item

    def check_conditions(self, game):
        return CommandEvent.check_conditions(self, game) and game.pc.has_item(self.__component_item_a) and game.pc.has_item(self.__component_item_b)

    def on_success(self, game):
        game.remove_item_from_player(self.__component_item_a)
        game.remove_item_from_player(self.__component_item_b)
        game.add_item_to_player(self.__result_item)
        game.iom.show_message(ps.MSG_DICT['ITEM_COMBINED_OK'])


class UseItemWithItemEvent(CommandEvent):
    """ Event to use a pair of items.

    A pysud user must inherit and implement the on_success() method.
    """
    def __init__(self, item_a, item_b):
        self.__item_a = item_a
        self.__item_b = item_b
        cmd = ps.complex_map(ps.CMD_ITEM_USE, self.__item_a.name, self.__item_b.name)
        CommandEvent.__init__(self, commands = cmd)

    def check_conditions(self, game):
        return CommandEvent.check_conditions(self, game) and game.pc.has_item(self.__item_a) and game.pc.has_item(self.__item_b)

    def on_success(self, game):
        """ Abstract method. """


# Predefined global events:
class ShowPlayerInventoryEvent(CommandEvent):
    """  """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_SHOW_INVENTORY)

    def on_success(self, game):
        game.iom.show_player_inventory()


class ShowScoreEvent(CommandEvent):
    """  """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_SHOW_SCORE)

    def on_success(self, game):
        game.iom.show_score()


class QuitGameEvent(CommandEvent):
    """  """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_GAME_QUIT)

    def on_success(self, game):
        game.quit_game()


class SaveGameEvent(CommandEvent):
    """  """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_GAME_SAVE)

    def on_success(self, game):
        game.save_game()


class LoadGameEvent(CommandEvent):
    """  """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_GAME_LOAD)

    def on_success(self, game):
        game = game.load_game()


class ShowPlayerStatsEvent(CommandEvent):
    """  """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_SHOW_STATS)

    def on_success(self, game):
        game.iom.show_player_stats()

class ShowHelpEvent(CommandEvent):
    """  """
    def __init__(self):
        CommandEvent.__init__(self, commands = ps.CMD_SHOW_HELP)

    def on_success(self, game):
        game.iom.show_help()
