from colour import Color
from Game import *

if __name__ == "__main__":
    # players
    players = [Player(1, Color("red")), Player(2, Color("blue"))]

    # points
    _win_points = 50
    points = [0, 1, 2, 50, 4]

    game = Game(players, 5, points, _win_points)
    game.set_cell(1, 0, players[0])
    game.set_cell(1, 1, players[0])
    game.set_cell(2, 0, players[0])
    game.set_cell(0, 1, players[1])
    game.set_cell(0, 2, players[1])
    game.set_cell(0, 3, players[1])
    game.set_cell(1, 3, players[1])
    game.debug_print_board()
    game.debug_print_player_points()
