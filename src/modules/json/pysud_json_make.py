"""
"""

import pysud
import pysud_rooms_json_parser
import pysud_config_json_parser
import pysud_gm as gameMgr

CONFIG_FILE_PATH = 'config.json'
ROOMS_FILE_PATH = 'rooms.json'

if __name__ == '__main__':
    CFG_PARSER = pysud_config_json_parser.ConfigJsonParser(CONFIG_FILE_PATH)
    ROOMS_PARSER = pysud_rooms_json_parser.RoomsJsonParser(ROOMS_FILE_PATH)
    # parse configuration file:
    CFG_DICT = CFG_PARSER.parse()
    # parse rooms data file:
    ROOMS_LIST = ROOMS_PARSER.parse()
    # create a new game:
    GAME = pysud.Game(CFG_DICT['PLAYER_DEFAULT_NAME'])

    #
    # OLD VERSION:
    # CFG_DICT WAS NOT REALLY BEIGN USED : MSG ARE TAKEN FROM pysud_str
    # ENABLE JOURNAL AND ENABLE SAVEGAME AREN'T IMPLEMENTED INSIDE pysud
    # set game configuration:
    # GAME.iom.msg_dict = CFG_DICT
    #

    # add found rooms to the game:
    GAME.add_rooms(ROOMS_LIST)
    # create a game manager class object:
    GAME_MANAGER = gameMgr.GameManager(GAME)
    # use it to persist a game data file:
    GAME_MANAGER.save_game('game.data')
    # this data can be retrieved using pysud_gm.GameManager.load_game_data()
