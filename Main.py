from colour import Color
from Game import *

if __name__ == "__main__":
    # players
    players = [Player(1, Color("red")), Player(2, Color("blue"))]

    # points
    _win_points = 50
    points = [0, 0, 2, 10, 50]

    game = Game(players, 5, points, _win_points)
    game.set_cell(1, 0, players[0].get_color())
    game.set_cell(0, 1, players[1].get_color())
    game.debug_print_board()
