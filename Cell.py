class Cell:
    def __init__(self, x, y, player):
        self._direction_list = [1, 1, 1, 1]
        self._x = x
        self._y = y
        self._player = player

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    # gets 4-direction input and returns corresponding value
    def get_dir_value(self, direction):
        return self._direction_list[direction]

    def set_dir_value(self, direction, value):
        self._direction_list[direction] = value
