from Cell import *
from Directions import Direction, DirectionAccurate


class Board:
    # Constructor for the Board object
    def __init__(self, size):
        self._size = size
        self._board = []
        # Create empty matrix
        for i in range(self._size):
            self._board.append([None] * self._size)

    # Get size of the board
    def get_size(self):
        return self._size

    # Set the color of a cell
    # Returns >0 if color has been placed successfully, 0 otherwise
    def set_cell(self, x, y, player):
        assert self._board[y][x] is None
        self._board[y][x] = Cell(x, y, player)
        self.update_board(self._board[y][x])

    def get_cell(self, x, y):
        if x < 0 or y < 0 or x > self.get_size() or y > self.get_size():
            return None  # MAYBE DANGEROUS?!
        return self._board[y][x]

    # TODO: Update player points
    # Updates board cell lists from a starting cell
    def update_board(self, cell):
        # one for each DirectionAccurate, indicates whether it has been already updated
        already_managed_adjs = [False] * 8
        for direction in Direction:  # handle double adj case
            if self.check_double_adj(cell, direction):
                dir1, dir2 = Direction.generic_to_accurate(direction)
                self.update_sequence_double(cell, direction)
                already_managed_adjs[dir1] = True
                already_managed_adjs[dir2] = True

        for direction_accurate in DirectionAccurate:  # handle single adj case
            # TODO: check if same player
            if not already_managed_adjs[direction_accurate]:
                self.update_sequence(cell, direction_accurate)

    # updates values of a sequence of adjacent cells in both direction
    def update_sequence_double(self, start, direction_generic):
        dir1, dir2 = Direction.generic_to_accurate(direction_generic)
        neighbour1 = self.get_cell_in_direction(start, dir1)
        neighbour2 = self.get_cell_in_direction(start, dir2)
        updated_value = 1 + neighbour1.get_dir_value(direction_generic) + neighbour2.get_dir_value(direction_generic)
        start.set_dir_value(direction_generic, updated_value)

        while neighbour1 is not None:
            neighbour1.set_dir_value(direction_generic, updated_value)
            neighbour1 = self.get_cell_in_direction(neighbour1, dir1)
        while neighbour2 is not None:
            neighbour2.set_dir_value(direction_generic, updated_value)
            neighbour2 = self.get_cell_in_direction(neighbour2, dir2)

    # updates values of a sequence of adjacent cells in a specific direction
    # this function must be called only when placing a player color
    # also_update_start :: Bool
    def update_sequence(self, start, direction_accurate):
        next_cell = self.get_cell_in_direction(start, direction_accurate)
        if next_cell is not None:
            generic_dir = Direction.accurate_to_generic(direction_accurate)
            start.set_dir_value(generic_dir, next_cell.get_dir_value(generic_dir) + 1)

            while next_cell is not None:
                next_cell.set_dir_value(generic_dir, start.get_dir_value(generic_dir))
                next_cell = self.get_cell_in_direction(next_cell, direction_accurate)

    # returns cell object in direction direction_accurate from starting cell
    def get_cell_in_direction(self, cell, direction_accurate):
        if direction_accurate == DirectionAccurate.N:
            return self.get_cell(cell.get_x(), cell.get_y() + 1)
        if direction_accurate == DirectionAccurate.S:
            return self.get_cell(cell.get_x(), cell.get_y() - 1)
        if direction_accurate == DirectionAccurate.E:
            return self.get_cell(cell.get_x() + 1, cell.get_y())
        if direction_accurate == DirectionAccurate.W:
            return self.get_cell(cell.get_x() - 1, cell.get_y())
        if direction_accurate == DirectionAccurate.NE:
            return self.get_cell(cell.get_x() + 1, cell.get_y() + 1)
        if direction_accurate == DirectionAccurate.NW:
            return self.get_cell(cell.get_x() - 1, cell.get_y() + 1)
        if direction_accurate == DirectionAccurate.SE:
            return self.get_cell(cell.get_x() + 1, cell.get_y() - 1)
        if direction_accurate == DirectionAccurate.SW:
            return self.get_cell(cell.get_x() - 1, cell.get_y() - 1)

    # Checks if point has 2 adj in same Direction
    def check_double_adj(self, cell, direction):
        if direction == Direction.HORIZONTAL:
            return self.get_cell_in_direction(cell, DirectionAccurate.E) is not None and self.get_cell_in_direction(
                cell, DirectionAccurate.W) is not None
        elif direction == Direction.VERTICAL:
            return self.get_cell_in_direction(cell, DirectionAccurate.N) is not None and self.get_cell_in_direction(
                cell, DirectionAccurate.S) is not None
        elif direction == Direction.OBLIQUE_R:
            return self.get_cell_in_direction(cell, DirectionAccurate.NE) is not None and self.get_cell_in_direction(
                cell, DirectionAccurate.SW) is not None
        elif direction == Direction.OBLIQUE_L:
            return self.get_cell_in_direction(cell, DirectionAccurate.NW) is not None and self.get_cell_in_direction(
                cell, DirectionAccurate.SE) is not None

    def debug_print_board(self):
        for i in range(self.get_size()):
            for j in range(self.get_size()):
                if self.get_cell(i, j) is not None:
                    print(self.get_cell(i, j), end="")
                else:
                    print("-", end="")
            print()
