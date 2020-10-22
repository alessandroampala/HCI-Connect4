class Player:
    def __init__(self, name, color):
        self._color = color
        self._name = name
        self._points = 0

    def get_points(self):
        return self._points

    def get_color(self):
        return self._color

    def get_name(self):
        return self._name

    def set_points(self, points):
        self._points = points
