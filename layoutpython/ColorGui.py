from PyQt5 import QtWidgets, QtCore, QtGui, uic


class ColorGui(QtWidgets.QWidget):
    def __init__(self, player_button, player_colors):
        # Call the inherited classes __init__ method
        super(ColorGui, self).__init__()
        uic.loadUi("res/layout/color.ui", self)  # Load the .ui file
        # Remove the titlebar from the window and consider the widget as popup
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.move(QtGui.QCursor().pos())  # Move window to the cursor position
        # Change background color
        self.setStyleSheet("QWidget{\n	background-color:#47426b;\n}")

        self.player_colors = player_colors
        self.add_colors()

        self.show()  # Show the GUI

        self.player_button = player_button  # create a object variable for this button

    def add_colors(self):
        for x in range(len(self.player_colors)):
            for y in range(5):
                if x * 5 + y > len(self.player_colors) - 1:
                    break
                color_button = QtWidgets.QPushButton()
                color_button.setStyleSheet(
                    "background-color: " + self.player_colors[
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

    def color_button_pressed(self, color_button):
        self.player_colors.append(self.player_button.palette().color(
            QtGui.QPalette.Background).name())

        self.player_button.setStyleSheet(
            "border: 2px solid white; border-radius: 45px; background-color: " + color_button.palette(
            ).color(QtGui.QPalette.Background).name() + ";")  # get the background color of the button

        self.player_colors.remove(color_button.palette().color(
            QtGui.QPalette.Background).name())
