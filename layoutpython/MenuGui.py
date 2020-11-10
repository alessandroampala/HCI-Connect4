from PyQt5 import QtWidgets, QtCore, QtGui, uic
import Player
import Game
import layoutpython.ColorGui as Color_Gui
import layoutpython.GameGui as Game_Gui


class MenuGui(QtWidgets.QMainWindow):
    # Constructor for the main menu
    def __init__(self, screen_size):
        self._screen_size = screen_size
        self._player_colors = ["#e6194b", "#f58231", "#469990", "#ffe119", "#bfef45", "#3cb44b", "#42d4f4", "#4363d8",
                               "#911eb4", "#f032e6", "#a9a9a9", "#fabed4", "#ffd8b1", "#fffac8", "#aaffc3", "#dcbeff",
                               "#000000", "#800000", "#9a6324", "#808000"]
        self._players = 1
        self._row_points = 1

        super(MenuGui, self).__init__()
        uic.loadUi("res/layout/menu.ui", self)
        self.setWindowIcon(QtGui.QIcon("res/images/unito.png"))
        self.removePlayerButton.hide()
        self.removePointsButton.hide()
        self.show()

        self.new_player_button_pressed()
        self.new_player_button_pressed()
        self.new_point_button_pressed()
        self.connect_buttons()

    # Connects buttons to handlers
    def connect_buttons(self):
        self.newPlayerButton.clicked.connect(self.new_player_button_pressed)
        self.removePlayerButton.clicked.connect(self.remove_player_button_pressed)
        self.addPointsButton.clicked.connect(self.new_point_button_pressed)
        self.removePointsButton.clicked.connect(self.remove_point_button_pressed)
        self.playButton.clicked.connect(self.play_button_pressed)
        self.exitButton.clicked.connect(self.exit_button_pressed)

    # Creates a new player
    def new_player_button_pressed(self):
        player_container = QtWidgets.QVBoxLayout()
        player_container.setContentsMargins(5, 5, 5, 5)
        player_container.setSpacing(0)

        vertical_spacer_top = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        vertical_spacer_bottom = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        player_name = QtWidgets.QLineEdit()
        player_name.setStyleSheet("margin:10px 10px 0 10px;")
        player_name.setPlaceholderText("Player Name")
        player_name.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        player_name.setMaximumSize(150, 35)
        player_name.setMinimumSize(150, 35)
        player_name.setText("Player " + str(self._players))

        player_color = QtWidgets.QPushButton()
        player_color.setStyleSheet(
            "background-color: " + self._player_colors[0] + "; border: 2px solid white; border-radius: 45px;")
        player_color.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        player_color.setMaximumSize(90, 90)
        player_color.setMinimumSize(90, 90)
        player_color.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        player_color.clicked.connect(self.player_button_pressed)

        player_container.addItem(vertical_spacer_top)
        player_container.addWidget(
            player_color, alignment=QtCore.Qt.AlignCenter)
        player_container.addWidget(
            player_name, alignment=QtCore.Qt.AlignCenter)
        player_container.addItem(vertical_spacer_bottom)

        self.horizontalLayoutScrollArea.insertLayout(
            self._players, player_container)

        self._player_colors.pop(0)
        self._players += 1

        if self._players > 15:
            self.newPlayerButton.hide()

        if self._players > 3:
            self.removePlayerButton.show()

    # Button handler used to remove the latest player and add the color of the player to the available colors
    def remove_player_button_pressed(self):
        layout = self.horizontalLayoutScrollArea.itemAt(self._players - 1)

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtWidgets.QWidgetItem):
                widget = item.widget()
                if isinstance(widget, QtWidgets.QPushButton):
                    self._player_colors.append(widget.palette().color(QtGui.QPalette.Background).name())
                widget.close()

            layout.removeItem(item)

        self._players -= 1

        if self._players < 16:
            self.newPlayerButton.show()

        if self._players < 4:
            self.removePlayerButton.hide()

    # Adds new field for points based on a sequence of length self._row_points
    def new_point_button_pressed(self):
        sequence_length = QtWidgets.QLineEdit()
        sequence_length.setStyleSheet(
            "font-size:10pt")
        sequence_length.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sequence_length.setMaximumHeight(30)
        sequence_length.setMinimumHeight(30)
        sequence_length.setText(str(self._row_points))
        sequence_length.setEnabled(False)

        points = QtWidgets.QLineEdit()
        points.setStyleSheet(
            "font-size:10pt")
        points.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        points.setMaximumHeight(30)
        points.setMinimumHeight(30)

        self.pointsGridLayout.addWidget(sequence_length, self._row_points, 0)
        self.pointsGridLayout.addWidget(points, self._row_points, 1)

        self._row_points += 1

        if self._row_points > 10:
            self.addPointsButton.hide()

        if self._row_points > 2:
            self.removePointsButton.show()

    # Removes the last field for the sequence of length self._row_points-1
    def remove_point_button_pressed(self):
        for i in range(2):
            item = self.pointsGridLayout.itemAtPosition(self._row_points - 1, i)
            self.pointsGridLayout.itemAtPosition(self._row_points - 1, i).widget().close()
            self.pointsGridLayout.removeItem(item)

        self._row_points -= 1

        if self._row_points < 11:
            self.addPointsButton.show()

        if self._row_points < 3:
            self.removePointsButton.hide()

    # Opens the color picker window for the clicked player
    def player_button_pressed(self):
        color_widget = Color_Gui.ColorGui(self.sender(), self._player_colors)
        color_widget.show()

    # Hides the main menu and opens the game window
    def play_button_pressed(self):
        self.resultLabel.clear()
        sequence_points, size, points_to_win = self.get_settings()
        players = self.get_players()
        if players and sequence_points:
            play_window = Game_Gui.GameGui(Game.Game(players, size, sequence_points, points_to_win), self)
            play_window.show()
            self.hide()

    # Closes the main menu
    def exit_button_pressed(self):
        self.close()

    # Gets all the players from the gui
    def get_players(self):
        players = []
        for i in range(1, self._players):
            layout = self.horizontalLayoutScrollArea.itemAt(i)
            player_color = layout.itemAt(1).widget().palette().color(QtGui.QPalette.Background).name()
            player_name = layout.itemAt(2).widget().text()

            if player_name == "":
                self.resultLabel.setText(
                    "Please insert the player name for player: " + str(i))
                return []

            players.append(Player.Player(player_name, player_color))

        return players

    # Gets all the settings from the gui
    def get_settings(self):
        size = self.sizeLineEdit.text()
        points_to_win = self.pointsToWinLineEdit.text()
        sequence_points = []

        if not size.isnumeric() or int(size) > 15 or int(size) < 1:
            self.resultLabel.setText("Size should be a number. Min size = 1, Max size = 15")
            return [], 0, 0

        if not points_to_win.isnumeric() or int(points_to_win) > 1000 or int(points_to_win) < 1:
            self.resultLabel.setText(
                "Points to win should be a number. Min value = 1, Max value = 1000")
            return [], 0, 0

        for i in range(1, self._row_points):
            points = self.pointsGridLayout.itemAtPosition(i, 1).widget().text()

            if not points.isnumeric():
                if not sequence_points:
                    points = "0"
                else:
                    points = sequence_points[-1]
            elif int(points) > int(points_to_win):
                self.resultLabel.setText(
                    "Row: " + str(i) + " Max value = " + points_to_win)
                return [], 0, 0

            sequence_points.append(int(points))

        return sequence_points, int(size), int(points_to_win)

    def get_screen_size(self):
        return self._screen_size
