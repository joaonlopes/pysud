"""
pysud string module

Contains strings constants as well as string/lists handling helper functions
"""

CMD_LOOK = 'look', 'examine', 'inspect'
CMD_SHOW_SCORE = 'score',
CMD_SHOW_INVENTORY = 'i', 'inv'
CMD_SHOW_HELP = 'h', '?'
CMD_SHOW_STATS = 'stats', 'st'
CMD_GAME_LOAD = 'load', 'resume'
CMD_GAME_SAVE = 'save',
CMD_GAME_QUIT = 'quit', 'exit', 'qq'
CMD_ITEM_USE = 'use', 'u'
CMD_ITEM_GET = 'get', 'pickup', 'take'
CMD_ITEM_COMBINE = 'combine', 'merge'

# Default message strings dictionary:
MSG_DICT = dict()
MSG_DICT['PROMPT_TEXT'] = '~$>'
MSG_DICT['INVALID_CMD_TEXT'] = 'Invalid input'
MSG_DICT['HELP_TEXT'] = 'THIS IS THE HELP TEXT'
MSG_DICT['ROOM_ITEMS_STR'] = 'You see'
MSG_DICT['ROOM_EXITS_STR_1'] = 'You may go to'
MSG_DICT['ROOM_EXITS_STR_2'] = 'using'
MSG_DICT['PLAYER_INVENTORY_STR'] = 'You have:'
MSG_DICT['PLAYER_STATS_STR'] = 'Rooms visited:'
MSG_DICT['PLAYER_SCORE_STR'] = 'Your score is'
MSG_DICT['GAME_START_TEXT'] = 'Welcome'
MSG_DICT['GAME_RESUME_TEXT'] = 'welcome back'
MSG_DICT['GAME_END_TEXT'] = 'Goodbye!'
MSG_DICT['ITEM_RETRIEVED'] = 'You get'
MSG_DICT['ITEM_COMBINED_OK'] = 'Items successfully combined!'

# TODO docstring
DEFAULT_CONNECTOR = ' '


def simple_map(verbs, sust, connector=DEFAULT_CONNECTOR):
    expression = []
    for v in verbs:
        expression.append(v + connector + sust)
    return expression


def complex_map(verbs, first_sust, second_sust, connector=DEFAULT_CONNECTOR):
    expression = simple_map(simple_map(verbs,first_sust), second_sust, connector)
    for p in simple_map(verbs,second_sust):
        expression.append(p + connector + first_sust)
    return expression

if __name__ == '__main__':
    # unit test here (TODO asserts):
    print(tuple(complex_map(CMD_ITEM_COMBINE, 'flashlight', 'batteries', ' with ')))
    print(tuple(complex_map(['merge', 'fuse', 'combine'], 'flashlight', 'batteries', ' with ')))
    print(tuple(simple_map(['get', 'take', 'retrieve'], 'flashlight')))
