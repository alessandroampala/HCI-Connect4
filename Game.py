from Board import *


# players:  a list of Player object
# size: length of a single board row
# points: points list. Index represents the length, value the points associated
# win_points: points needed to win a game
def initialize(players, size, points, win_points):
    board = Board(size)
