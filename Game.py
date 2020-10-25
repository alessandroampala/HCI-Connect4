from Board import *
from Player import *


class Game:

    # players:  a list of Player object
    # size: length of a single board row
    # points: points list. Index represents the length, value the points associated
    # win_points: points needed to win a game
    def __init__(self, players, size, points, win_points):
        self._board = Board(size, points)
        self._players = players

    def get_players(self):
        return self._players

    def get_size(self):
        return self._board.get_size()

    def get_cell(self, x, y):
        return self._board.get_cell(x, y)

    def set_cell(self, x, y, player):
        self._board.set_cell(x, y, player)

    # Return true if game ended
    def game_ended(self):
        assert False
        return  # replace with end condition