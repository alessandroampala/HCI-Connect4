class Player:
    def __init__(self, name, color):
        self._color = color
        self._name = name
        self._points = 0

    # Get player points
    def get_points(self):
        return self._points

    # Get player color
    def get_color(self):
        return self._color

    # Get player name
    def get_name(self):
        return self._name

    # Set player points
    def set_points(self, points):
        self._points = points
