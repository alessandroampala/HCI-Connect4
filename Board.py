from Cell import *
from Directions import Direction, DirectionAccurate


class Board:
    # Constructor for the Board object
    # size: length of a single board row
    # sequence_points: points list. Index represents the length, value the points associated
    def __init__(self, size, sequence_points):
        """size: length of a single board row. sequence_points: points list. Index represents the length, value the points associated"""
        self._size = size
        self._board = []
        self._sequence_points = sequence_points
        self._empty_cells = size * size
        # Create empty matrix
        for i in range(self._size):
            self._board.append([None] * self._size)

    # Get size of the board
    def get_size(self):
        """Get size of the board"""
        return self._size

    # Set the color of a cell
    def set_cell(self, x, y, player):
        """Set the color of a cell"""
        assert self._board[x][y] is None
        self._board[x][y] = Cell(x, y, player)
        self.update_board(self._board[x][y])
        self._empty_cells -= 1

    # Returns Cell object in the specified position
    def get_cell(self, x, y):
        """Returns Cell object in the specified position"""
        if x < 0 or y < 0 or x >= self.get_size() or y >= self.get_size():
            return None  # MAYBE DANGEROUS?!
        return self._board[x][y]

    # Corresponding points for a sequence of length sequence_length
    def get_sequence_points(self, sequence_length):
        """Corresponding points for a sequence of length sequence_length"""
        length = len(self._sequence_points)
        if sequence_length >= length:
            return self._sequence_points[length - 1]
        return self._sequence_points[sequence_length]

    # Updates board sequences from a new, just-placed starting cell
    def update_board(self, cell):
        """Updates board sequences from a new, just-placed starting cell"""
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

    # updates direction_list values of a sequence of adjacent cells in both direction
    # this function must be called only when placing a player color
    def update_sequence_double(self, start, direction_generic):
        """updates direction_list values of a sequence of adjacent cells in both direction.
        this function must be called only when placing a player color"""
        dir1, dir2 = Direction.generic_to_accurate(direction_generic)
        neighbour1 = self.get_cell_in_direction(start, dir1)
        neighbour2 = self.get_cell_in_direction(start, dir2)
        old_value1 = neighbour1.get_dir_value(direction_generic)
        old_value2 = neighbour2.get_dir_value(direction_generic)
        updated_value = 1 + old_value1 + old_value2
        start.set_dir_value(direction_generic, updated_value)  # Update cell's direction value
        player = start.get_player()  # Get start's Player object

        new_points = 0
        # Subtract old points only if the placement of that cell added points for a 1-length sequence
        if not (old_value1 == 1 and not neighbour1.is_isolated()):
            new_points += -self.get_sequence_points(old_value1)
        if not (old_value2 == 1 and not neighbour2.is_isolated()):
            new_points += -self.get_sequence_points(old_value2)

        new_points += player.get_points() + self.get_sequence_points(1 + old_value1 + old_value2)
        player.set_points(new_points)

        while neighbour1 is not None and start.same_player_as(neighbour1):
            neighbour1.set_dir_value(direction_generic, updated_value)
            neighbour1 = self.get_cell_in_direction(neighbour1, dir1)
        while neighbour2 is not None and start.same_player_as(neighbour2):
            neighbour2.set_dir_value(direction_generic, updated_value)
            neighbour2 = self.get_cell_in_direction(neighbour2, dir2)

    # updates direction_list values of a sequence of adjacent cells in a specific direction
    # this function must be called only when placing a player color
    def update_sequence(self, start, direction_accurate):
        """updates direction_list values of a sequence of adjacent cells in a specific direction.
        this function must be called only when placing a player color"""
        next_cell = self.get_cell_in_direction(start, direction_accurate)
        if next_cell is not None:
            generic_dir = Direction.accurate_to_generic(direction_accurate)
            next_cell_value = next_cell.get_dir_value(generic_dir)
            start.set_dir_value(generic_dir, next_cell_value + 1)
            player = start.get_player()
            if next_cell_value == 1 and not next_cell.is_isolated():
                new_points = player.get_points() + self.get_sequence_points(next_cell_value + 1)
            else:
                new_points = player.get_points() - self.get_sequence_points(next_cell_value) + self.get_sequence_points(next_cell_value + 1)

            player.set_points(new_points)

            while next_cell is not None and start.same_player_as(next_cell):
                next_cell.set_dir_value(generic_dir, start.get_dir_value(generic_dir))
                next_cell = self.get_cell_in_direction(next_cell, direction_accurate)

    # returns cell object in direction direction_accurate from starting cell
    def get_cell_in_direction(self, cell, direction_accurate):
        """returns cell object in direction direction_accurate from starting cell"""
        if direction_accurate == DirectionAccurate.N:
            return self.get_cell(cell.get_x(), cell.get_y() - 1)
        if direction_accurate == DirectionAccurate.S:
            return self.get_cell(cell.get_x(), cell.get_y() + 1)
        if direction_accurate == DirectionAccurate.E:
            return self.get_cell(cell.get_x() + 1, cell.get_y())
        if direction_accurate == DirectionAccurate.W:
            return self.get_cell(cell.get_x() - 1, cell.get_y())
        if direction_accurate == DirectionAccurate.NE:
            return self.get_cell(cell.get_x() + 1, cell.get_y() - 1)
        if direction_accurate == DirectionAccurate.NW:
            return self.get_cell(cell.get_x() - 1, cell.get_y() - 1)
        if direction_accurate == DirectionAccurate.SE:
            return self.get_cell(cell.get_x() + 1, cell.get_y() + 1)
        if direction_accurate == DirectionAccurate.SW:
            return self.get_cell(cell.get_x() - 1, cell.get_y() + 1)

    # Checks if point has 2 adj in same Direction
    def check_double_adj(self, cell, direction):
        """Checks if point has 2 adj in same Direction"""
        for generic in Direction:
            if direction == generic:
                dir1, dir2 = Direction.generic_to_accurate(generic)
                neighbour1 = self.get_cell_in_direction(cell, dir1)
                neighbour2 = self.get_cell_in_direction(cell, dir2)
                return neighbour1 is not None and neighbour2 is not None and cell.same_player_as(neighbour1) and cell.same_player_as(neighbour2)

    # Returns True if all the cells have been placed
    def is_full(self):
        """Returns True if all the cells have been placed"""
        return self._empty_cells == 0

    def debug_print_board(self):
        for i in range(self.get_size()):
            for j in range(self.get_size()):
                if self.get_cell(i, j) is not None:
                    print(self.get_cell(i, j), end="")
                else:
                    print("-", end="")
            print()
