class Cell:
    # x, y specifies the position of the cell
    # player: the player that placed a color on this cell
    def __init__(self, x, y, player):
        """x, y specifies the position of the cell.
        player: the player that placed a color on this cell"""
        self._direction_list = [1, 1, 1, 1]
        self._x = x
        self._y = y
        self._player = player

    # Get x component of cell's position
    def get_x(self):
        """Get x component of cell's position"""
        return self._x

    # Get y component of cell's position
    def get_y(self):
        """Get y component of cell's position"""
        return self._y

    # Returns the value associated to the generic direction parameter
    def get_dir_value(self, direction):
        """Returns the value associated to the generic direction parameter"""
        return self._direction_list[direction]

    # Sets the value associated to the generic direction parameter
    def set_dir_value(self, direction, value):
        """Sets the value associated to the generic direction parameter"""
        self._direction_list[direction] = value

    # Return Player object that placed a color on this cell
    def get_player(self):
        """Return Player object that placed a color on this cell"""
        return self._player

    # Returns True if self and cell belong to the same player
    def same_player_as(self, cell):
        """Returns True if self and cell belong to the same player"""
        return self._player == cell.get_player()

    # Returns True if this cell has no adjacent cells
    def is_isolated(self):
        """Returns True if this cell has no adjacent cells"""
        for val in self._direction_list:
            if val > 1:
                return False
        return True
