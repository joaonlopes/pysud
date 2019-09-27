import json
import pysud

class RoomsJsonParser():
    """
    Summary
    Attributes:
        rooms_json_file:    A valid json file path containing pysud rooms.
    """
    def __init__(self, rooms_json_file_path):
        self.rooms_json_file = json.load(open(rooms_json_file_path, 'r', encoding='utf-8'))

    def build_rooms_dict(self):
        """
        Parses a rooms json.

        Returns:
            A dictionary containing all found rooms, indexed by room id.
        """
        rooms_dict = dict()
        for room_json in self.rooms_json_file:
            # rooms found in json must be converted to pysud Room objects:
            room = pysud.Room(room_json['name'], room_json['description'], room_json['id'])
            rooms_dict[room.get_id()] = room
        return rooms_dict


    def link_rooms(self, rooms_dict):
        """ Links rooms trhough transitions.

        Args:
            rooms_dict: An id indexed rooms collection.
        Returns:
            A list containing all rooms found on file, conected between them via transitions.
        """
        rooms_list = list()
        for room_json in self.rooms_json_file:
            origin_room_id = room_json['id']
            origin_room = rooms_dict[origin_room_id]
            # transitions found will be used to create pysud.Transition objects
            # this requires all rooms to be loaded first
            if ('transitions' in room_json):
                for transition_json in room_json['transitions']:
                    destination_room_id = transition_json['destination']
                    destination_room = rooms_dict[destination_room_id]
                    commands = transition_json['commands']
                    origin_room.add_transition(commands, destination_room)
            rooms_list.append(origin_room)
        return rooms_list

    def parse(self):
        return self.link_rooms(self.build_rooms_dict())

# Testing purposes: run this script in a directory containing a valid rooms.json file
# running python3 in interative mode might be a good idea
if __name__ == '__main__':
    ROOMS_FILE = 'rooms.json'
    rooms_json_parser = RoomsJsonParser(ROOMS_FILE)
    rooms = rooms_json_parser.parse()
    rooms_json_parser = None
    print('Rooms found: ' + str(rooms))
