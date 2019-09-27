
"""
XML pysud module.

Provides classes to deal with xml data files.
"""

import xml.etree.ElementTree as etree
import pysud


class XMLParser():
    """
    Abstract class to provide basic xml files handling functionality.

    Attributes:
        xml_file:    A valid xml file path.
        xml_root:    ElementTree Root class object.
    """
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.xml_root = None

    def parse_file(self):
        pass


class ConfigXMLParser(XMLParser):
    """ This class handles all config.xml file parsing. """
    def parse_file(self):
        """
        Parses main configuration xml.

        Returns:
            A dictionary containing configuration values.
            (This configuration values should be mapped to
             a pysud.Game class object instance variables)
        """
        tree = etree.parse(self.xml_file)
        self.xml_root = tree.getroot()
        config = dict()
        config['ENABLE_JOURNAL'] = self.xml_root.find('ENABLE_JOURNAL').text
        config['ENABLE_SAVEGAME'] = self.xml_root.find('ENABLE_SAVEGAME').text
        config['HELP_TEXT'] = self.xml_root.find('HELP_TEXT').text
        config['INVALID_CMD_TEXT'] = self.xml_root.find('INVALID_CMD_TEXT').text
        config['PROMPT_TEXT'] = self.xml_root.find('PROMPT_TEXT').text
        config['GAME_START_TEXT'] = self.xml_root.find('GAME_START_TEXT').text
        config['GAME_RESUME_TEXT'] = self.xml_root.find('GAME_RESUME_TEXT').text
        config['GAME_END_TEXT'] = self.xml_root.find('GAME_END_TEXT').text
        config['PLAYER_DEFAULT_NAME'] = self.xml_root.find('PLAYER_DEFAULT_NAME').text
        config['ROOM_ITEMS_STR'] = self.xml_root.find('ROOM_ITEMS_STR').text
        config['PLAYER_SCORE_STR'] = self.xml_root.find('PLAYER_SCORE_STR').text
        config['PLAYER_INVENTORY_STR'] = self.xml_root.find('PLAYER_INVENTORY_STR').text
        config['PLAYER_STATS_STR'] = self.xml_root.find('PLAYER_STATS_STR').text
        return config


class RoomsXMLParser(XMLParser):
    """ This class handles all rooms.xml file parsing. """
    def parse_file(self):
        """
        Parses rooms definition file.

        Returns:
            A python List holding pysud.Room class objects
        """
        tree = etree.parse(self.xml_file)
        self.xml_root = tree.getroot()
        rooms_data = dict()
        for room_tag in self.xml_root:
            temp = self.__parse_room(room_tag)
            rooms_data[temp[0].get_id()] = temp
        return self.__link_rooms(rooms_data)

    def __link_rooms(self, rooms_data):
        """ Associates each rooms with its transitions.

        Args:
            rooms_data: a python Dictionary composed by:
                key : a pysud.Room Id
                value : a pair ( Room class object, transition List for that room )

        Returns:
            A python List holding pysud.Room class objects
        """
        res = list()
        for p in rooms_data.values():
            if p[1] != None:
                for transition_stub in p[1]:
                    destination_room = rooms_data.get(transition_stub.destination)[0]
                    commands = transition_stub.get_commands()
                    p[0].add_transition(commands, destination_room)
            res.append(p[0])
        return res

    def __parse_room(self, room_tag):
        """
        Parses a (single) room xml tag.

        Args:
            room_tag: The room xml tag to parse
        Returns:
            A python Tuple containing:
                a pysud.rooms object
                a python list
        """
        room_description = None
        room_name = room_tag.get('name')
        room_id = room_tag.get('id')
        room_transitions = None
        for element in room_tag.getchildren():
            if element.tag == 'description':
                room_description = element.text
            elif element.tag == 'transitions':
                # self.print_transitions(element, room_id)
                room_transitions = self.__parse_transition(element, room_id)
            else:
                pass  # invalid tag found
        room = pysud.Room(room_name, room_description, room_id)
        return tuple(room, room_transitions)

    def __parse_transition(self, transitions_tag, room_origin_id):
        l = list()
        # iterates over a given room destinations:
        for transition in transitions_tag.getchildren():
            room_destination_id = transition.get('destination')
            ts = TransitionStub(room_origin_id, room_destination_id)
            # iterates over a single destination alias commands:
            for command in transition.getchildren():
                ts.add_command(command.text)
            l.append(ts)
        return l

    def print_transitions(self, transitions_tag, room_origin_id):
        print('from ', room_origin_id, ' you can go to:')
        # iterates over a given room destinations:
        for transition in transitions_tag.getchildren():
            dest = transition.get('destination')
            print('\t', dest)
            # iterates over a single destination alias commands:
            for com in transition.getchildren():
                print('\t\t with commands:', com.text)


class TransitionStub:
    """ Internal class to hold a single transition data.

    An object instance of this class is used exclusively to temporarily hold
    parsed data for a room transition."""
    def __init__(self, origin_room_id , destination_room_id):
        self.origin = origin_room_id
        self.destination = destination_room_id
        self.__commands = list()

    def add_command(self, command):
        self.__commands.append(command)

    def get_commands(self):
        return self.__commands

# @DEBUG - For testing purposes only:
if __name__ == '__main__':
    CFG_XML_FILE = 'config.xml'
    ROOMS_XML_FILE = 'rooms.xml'
    C = ConfigXMLParser(CFG_XML_FILE)
    RP = RoomsXMLParser (ROOMS_XML_FILE)
    R = RP.parse_file()
    E = RP.xml_root
