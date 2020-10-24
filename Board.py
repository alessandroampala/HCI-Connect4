from Cell import *
from Directions import Direction, DirectionAccurate


class Board:
    # Constructor for the Board object
    def __init__(self, size, sequence_points):
        self._size = size
        self._board = []
        self._sequence_points = sequence_points
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

    def get_sequence_points(self, sequence_length):
        length = len(self._sequence_points)
        if sequence_length > length:
            return self._sequence_points[length - 1]
        return self._sequence_points[sequence_length]

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
            current = self.get_cell_in_direction(cell, direction_accurate)
            if not already_managed_adjs[direction_accurate] and current is not None and cell.same_player_as(current):
                self.update_sequence(cell, direction_accurate)
                already_managed_adjs[direction_accurate] = True

        # Check if no adjacents
        all_false = False
        for boolean in already_managed_adjs:
            all_false = all_false or boolean
        if not all_false:
            cell.get_player().set_points(cell.get_player().get_points() + self.get_sequence_points(1))

    # updates values of a sequence of adjacent cells in both direction
    def update_sequence_double(self, start, direction_generic):
        dir1, dir2 = Direction.generic_to_accurate(direction_generic)
        neighbour1 = self.get_cell_in_direction(start, dir1)
        neighbour2 = self.get_cell_in_direction(start, dir2)
        old_value1 = neighbour1.get_dir_value(direction_generic)
        old_value2 = neighbour2.get_dir_value(direction_generic)
        updated_value = 1 + old_value1 + old_value2
        start.set_dir_value(direction_generic, updated_value)  # Update cell's direction value
        player = start.get_player()  # Get start's Player object
        new_points = player.get_points() - self.get_sequence_points(old_value1) - self.get_sequence_points(old_value2) + self.get_sequence_points(1 + old_value1 + old_value2)
        player.set_points(new_points)

        while neighbour1 is not None and start.same_player_as(neighbour1):
            neighbour1.set_dir_value(direction_generic, updated_value)
            neighbour1 = self.get_cell_in_direction(neighbour1, dir1)
        while neighbour2 is not None and start.same_player_as(neighbour2):
            neighbour2.set_dir_value(direction_generic, updated_value)
            neighbour2 = self.get_cell_in_direction(neighbour2, dir2)

    # updates values of a sequence of adjacent cells in a specific direction
    # this function must be called only when placing a player color
    # also_update_start :: Bool
    def update_sequence(self, start, direction_accurate):
        next_cell = self.get_cell_in_direction(start, direction_accurate)
        if next_cell is not None:
            generic_dir = Direction.accurate_to_generic(direction_accurate)
            next_cell_value = next_cell.get_dir_value(generic_dir)
            start.set_dir_value(generic_dir, next_cell_value + 1)
            player = start.get_player()
            new_points = player.get_points() - next_cell_value + self.get_sequence_points(next_cell_value + 1)
            player.set_points(new_points)

            while next_cell is not None and start.same_player_as(next_cell):
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
        for generic in Direction:
            if direction == generic:
                dir1, dir2 = Direction.generic_to_accurate(generic)
                neighbour1 = self.get_cell_in_direction(cell, dir1)
                neighbour2 = self.get_cell_in_direction(cell, dir2)
                return neighbour1 is not None and neighbour2 is not None and cell.same_player_as(neighbour1) and cell.same_player_as(neighbour2)

    def debug_print_board(self):
        for i in range(self.get_size()):
            for j in range(self.get_size()):
                if self.get_cell(i, j) is not None:
                    print(self.get_cell(i, j), end="")
                else:
                    print("-", end="")
            print()
