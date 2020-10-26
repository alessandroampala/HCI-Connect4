from Board import *
from Player import *


class Game:

    # players:  a list of Player object
    # size: length of a single board row
    # points: points list. Index represents the length, value the points associated
    # win_points: points needed to win a game
    def __init__(self, players, size, points, win_points):
        points = [0] + points
        self._board = Board(size, points)
        self._players = players
        self._win_points = win_points
        self._winner = None

    # Returns Cell object in the specified position
    def get_cell(self, x, y):
        return self._board.get_cell(x, y)

    # Set the color of a cell
    def set_cell(self, x, y, player):
        self._board.set_cell(x, y, player)
    
    # Returns players list
    def get_players(self):
        return self._players

    # Returns size of the board
    def get_size(self):
        return self._board.get_size()

    # Returns True if game ended
    # If this returns true, the get_winner method will return the winner Player
    def game_ended(self):
        """Returns True if game ended.
        If this returns true, the get_winner method will return the winner Player"""
        for player in self._players:
            if player.get_points() >= self._win_points:
                self._winner = player
                return True
        return False

    # Returns the Player that won the game
    def get_winner(self):
        return self._winner

    def debug_print_board(self):
        self._board.debug_print_board()

    def debug_print_player_points(self):
        for player in self._players:
            print("Player" + str(player.get_name()) + ": " + str(player.get_points()))