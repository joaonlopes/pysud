import json
import pysud

class ConfigJsonParser():
    """
    Summary
    Attributes:
        config_json_file:    A valid json file path containing pysud game configurations.
    """

    def __init__(self, config_json_file_path):
        self.config_json_file = json.load(open(config_json_file_path, 'r', encoding='utf-8'))

    def parse(self):
        configurations_json = self.config_json_file['config']
        config_dict = dict()
        config_dict['ENABLE_JOURNAL'] = configurations_json['ENABLE_JOURNAL']
        config_dict['ENABLE_SAVEGAME'] = configurations_json['ENABLE_SAVEGAME']
        config_dict['PLAYER_DEFAULT_NAME'] = configurations_json['PLAYER_DEFAULT_NAME']
        return config_dict


########################################################################
# Testing purposes:                                                    #
# run this script in a directory containing a valid config.json file   #
# along with the pysud basic modules                                   #
# python3 -i config_json_parser.py                                     #
########################################################################
if __name__ == '__main__':
    CONFIG_FILE = 'config.json'
    config_json_parser = ConfigJsonParser(CONFIG_FILE)
    config = config_json_parser.parse()
    config_json_parser = None
    print('Configurations found: ' + str(config))
