
"""
Provides GameManager class to handle persistance and misc.
"""

import shelve

class GameManager():
    """ GameManager class. A wrapper for pysud.Game class.

    Mostly manages object's persistance.
    When possible, a pysud user must communicate with her game through
    this class

    Attributes:

        game: pysud.Game class instance.
    """

    def __init__(self, new_game):
        self.game = None
        self.link_with_game(new_game)

    def run_game(self):
        self.game.run_game()

    def resume_game(self):
        self.game.resume_game()

    def save_game(self, filename = 'save.data'):
        """ Saves the current game state.

        Args:
            filename: Of file to be created.
        """
        dest_file = shelve.open(filename)
        self.game.clear_game_mgr()  # Avoid persisting the game manager
        dest_file['data'] = self.game
        dest_file.close()
        self.game.set_game_mgr(self)

    def load_game(self, filename = 'save.data'):
        """ Loads a previous game and resumes its execution.

        Args:
            filename: Of file to be loaded.
        """
        self.load_game_data(filename)
        self.game.iom.show_welcome_back_message()
        self.resume_game()

    def load_game_data(self, filename = 'save.data'):
        """ Loads a game data file without starting it.

        Args:
            filename: Of file to be loaded.
        """
        self.game.stop_game()
        game_file = shelve.open(filename)
        new_game = game_file['data']
        game_file.close()
        self.link_with_game(new_game)

    def link_with_game(self, new_game):
        new_game.set_game_mgr(self)
        self.game = new_game
