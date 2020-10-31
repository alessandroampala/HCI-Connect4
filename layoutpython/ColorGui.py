from PyQt5 import QtWidgets, QtCore, QtGui, uic


class ColorGui(QtWidgets.QWidget):
    # Constructor for the color picker
    # player_button -> player that want to change his color
    # player_colors -> available colors for the color picker
    def __init__(self, player_button, player_colors):
        self._player_colors = player_colors
        self._player_button = player_button

        super(ColorGui, self).__init__()
        uic.loadUi("res/layout/color.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.move(QtGui.QCursor().pos())
        self.setStyleSheet("QWidget{\n	background-color:#47426b;\n}")
        self.add_colors()
        self.show()

    # Adds colors to the view as buttons and connects it to an handler
    def add_colors(self):
        for x in range(len(self._player_colors)):
            for y in range(5):
                if x * 5 + y > len(self._player_colors) - 1:
                    break

                color_button = QtWidgets.QPushButton()
                color_button.setStyleSheet(
                    "background-color: " + self._player_colors[
                        x * 5 + y] + "; border: 2px solid white; border-radius: 15px;")
                color_button.setSizePolicy(
                    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                color_button.setMaximumSize(30, 30)
                color_button.setMinimumSize(30, 30)
                color_button.setCursor(QtGui.QCursor(
                    QtCore.Qt.PointingHandCursor))

                color_button.clicked.connect(
                    lambda: self.color_button_pressed(self.sender()))

                self.colorsLayout.addWidget(color_button, x, y)

    # Manages the button clicked: Sets the color for the player; Removes chosen color from the player_colors list;
    # color_button -> Button clicked by the player
    def color_button_pressed(self, color_button):
        self._player_colors.append(self._player_button.palette().color(
            QtGui.QPalette.Background).name())

        self._player_button.setStyleSheet(
            "border: 2px solid white; border-radius: 45px; background-color: " + color_button.palette(
            ).color(QtGui.QPalette.Background).name() + ";")  # get the background color of the button

        self._player_colors.remove(color_button.palette().color(
            QtGui.QPalette.Background).name())
