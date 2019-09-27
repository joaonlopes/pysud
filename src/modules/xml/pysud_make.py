
"""
MakeGameData pysud module.

Uses pysud_xml and other modules to create a new (initial) game data file.
"""

import pysud
import pysud_xml
import pysud_gm as gameMgr

# Path to main configuration xml file:
CONFIG_XML_PATH = 'config.xml'
# Path to rooms definitions xml file:
ROOMS_XML_PATH = 'rooms.xml'

def set_game_configs(game, configs_dict):
    game.iom.msg_dict = configs_dict

if __name__ == '__main__':
    CFG_PARSER = pysud_xml.ConfigXMLParser(CONFIG_XML_PATH)
    ROOMS_PARSER = pysud_xml.RoomsXMLParser(ROOMS_XML_PATH)
    # parse configuration file:
    CFG_DICT = CFG_PARSER.parse_file()
    # parse rooms data file:
    ROOMS_LIST = ROOMS_PARSER.parse_file()
    # create a new game:
    GAME = pysud.Game(CFG_DICT['PLAYER_DEFAULT_NAME'])
    # set game configuration:
    set_game_configs(GAME, CFG_DICT)
    # add found rooms to the game:
    GAME.add_rooms(ROOMS_LIST)
    # create a game manager class object:
    GAME_MANAGER = gameMgr.GameManager(GAME)
    # use it to persist a data file:
    GAME_MANAGER.save_game('game.data')
    #   this data can be retrieved using
    #   pysud_gm.GameManager.load_game_data()
