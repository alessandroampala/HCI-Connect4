class Player:
    # name: the name of the player
    # color: the color associated
    def __init__(self, name, color):
        """name: the name of the player.
        color: the color associated"""
        self._color = color
        self._name = name
        self._points = 0

    # Get player points
    def get_points(self):
        """Get player points"""
        return self._points

    # Get player color
    def get_color(self):
        """Get player color"""
        return self._color

    # Get player name
    def get_name(self):
        """Get player name"""
        return self._name

    # Set player points
    def set_points(self, points):
        """Set player points"""
        self._points = points
