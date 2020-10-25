import sys

from PyQt5 import QtWidgets, QtCore, QtGui, uic
import Player
import Board
import Game
import layoutpython.ColorGui as Color_Gui
import layoutpython.GameGui as GameGui


class MenuGui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(MenuGui, self).__init__()
        uic.loadUi("res/layout/menu.ui", self)  # Load the .ui file

        self.player_colors = ["#000000", "#800000", "#9a6324", "#808000", "#469990", "#e6194b", "#f58231", "#ffe119",
                              "#bfef45", "#3cb44b", "#42d4f4", "#4363d8", "#911eb4", "#f032e6", "#a9a9a9", "#fabed4",
                              "#ffd8b1", "#fffac8", "#aaffc3", "#dcbeff"]
        self.players = 1
        self.new_player()
        self.new_player()

        self.row_points = 2

        self.setWindowIcon(QtGui.QIcon("res/images/unito.png"))

        self.removePlayerButton.hide()
        self.removePointsButton.hide()

        self.show()  # Show the GUI

        self.newPlayerButton.clicked.connect(self.new_player_button_pressed)

        self.removePlayerButton.clicked.connect(self.remove_player_button_pressed)

        self.addPointsButton.clicked.connect(self.new_point_button_pressed)

        self.removePointsButton.clicked.connect(self.remove_point_button_pressed)

        self.playButton.clicked.connect(self.play_button_pressed)

        self.exitButton.clicked.connect(self.exit_button_pressed)

    def new_player(self):
        player_container = QtWidgets.QVBoxLayout()
        player_container.setContentsMargins(5, 5, 5, 5)
        player_container.setSpacing(0)

        vertical_spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        player_name = QtWidgets.QLineEdit()
        player_name.setStyleSheet("margin:10px 10px 0 10px;")
        player_name.setPlaceholderText("Player Name")
        player_name.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        player_name.setMaximumSize(150, 35)
        player_name.setMinimumSize(150, 35)
        player_name.setText("Player " + str(self.players))

        player_color = QtWidgets.QPushButton()
        player_color.setStyleSheet(
            "background-color: " + self.player_colors[0] + "; border: 2px solid white; border-radius: 45px;")
        player_color.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        player_color.setMaximumSize(90, 90)
        player_color.setMinimumSize(90, 90)
        player_color.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        player_color.clicked.connect(self.player_button_pressed)

        player_container.addItem(vertical_spacer)
        player_container.addWidget(
            player_color, alignment=QtCore.Qt.AlignCenter)
        player_container.addWidget(
            player_name, alignment=QtCore.Qt.AlignCenter)
        player_container.addItem(vertical_spacer)

        self.horizontalLayoutScrollArea.insertLayout(
            self.players, player_container)
        self.player_colors.pop(0)
        self.players += 1

        if self.players > 15:
            self.newPlayerButton.hide()

        if self.players > 3:
            self.removePlayerButton.show()

    def remove_player_button_pressed(self):
        print("remove_player_button_pressed")
        layout = self.horizontalLayoutScrollArea.itemAt(self.players - 1)

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtWidgets.QWidgetItem):
                widget = item.widget()
                if isinstance(widget, QtWidgets.QPushButton):
                    self.player_colors.append(widget.palette().color(QtGui.QPalette.Background).name())
                widget.close()

            layout.removeItem(item)

        self.players -= 1

        if self.players < 16:
            self.newPlayerButton.show()

        if self.players < 4:
            self.removePlayerButton.hide()

    def new_point_button_pressed(self):
        print("new_point_button_pressed")
        sequence_length = QtWidgets.QLineEdit()
        sequence_length.setStyleSheet(
            "font-size:10pt")
        sequence_length.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sequence_length.setMaximumHeight(30)
        sequence_length.setMinimumHeight(30)
        sequence_length.setText(str(self.row_points-1))
        sequence_length.setEnabled(False)

        points = QtWidgets.QLineEdit()
        points.setStyleSheet(
            "font-size:10pt")
        points.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        points.setMaximumHeight(30)
        points.setMinimumHeight(30)

        self.pointsGridLayout.addWidget(sequence_length, self.row_points, 0)
        self.pointsGridLayout.addWidget(points, self.row_points, 1)

        self.row_points += 1

        if self.row_points > 10:
            self.addPointsButton.hide()

        if self.row_points > 2:
            self.removePointsButton.show()

    def remove_point_button_pressed(self):
        print("remove_point_button_pressed")

        for i in range(2):
            item = self.pointsGridLayout.itemAtPosition(  self.row_points-1, i)
            self.pointsGridLayout.itemAtPosition(  self.row_points-1, i).widget().close()
            self.pointsGridLayout.removeItem(item)

        self.row_points -= 1

        if self.row_points < 11:
            self.addPointsButton.show()

        if self.row_points < 3:
            self.removePointsButton.hide()

    def player_button_pressed(self):
        print("player_button_pressed")
        color_widget = Color_Gui.ColorGui(self.sender(), self.player_colors)
        color_widget.show()

    def new_player_button_pressed(self):
        print("new_player_button_pressed")
        self.new_player()

    def play_button_pressed(self):
        print("play_button_pressed")
        self.resultLabel.clear()
        sequence_points, size, points_to_win = self.get_settings()
        players = self.get_players()
        if players and sequence_points:
            play_widget = GameGui.GameGui(Game.Game(players, size, sequence_points, points_to_win), self)
            play_widget.show()
            self.hide()

    def exit_button_pressed(self):
        print("exit_button_pressed")
        self.close()

    def get_players(self):
        players = []
        for i in range(1, self.players):
            layout = self.horizontalLayoutScrollArea.itemAt(i)
            player_color = layout.itemAt(1).widget().palette().color(
                QtGui.QPalette.Background).name()
            player_name = layout.itemAt(2).widget().text()

            if player_name == "":
                self.resultLabel.setText(
                    "Please insert the player name for player: " + str(i))
                print(
                    "Please insert the player name for player: " + str(i))
                return []

            players.append(Player.Player(player_name, player_color))

        return players

    def get_settings(self):
        size = self.sizeLineEdit.text()
        points_to_win = self.pointsToWinLineEdit.text()
        sequence_points = []

        if not size.isnumeric() or int(size) > 15:
            self.resultLabel.setText("Size should be a number. Max size = 15")
            print("Size should be a number. Max size = 15")
            return [], 0, 0

        if not points_to_win.isnumeric() or int(points_to_win) > 1000:
            self.resultLabel.setText(
                "Points to win should be a number. Max value = 1000")
            print("Points to win should be a number. Max value = 1000")
            return [], 0, 0

        for i in range(1, self.row_points):
            sequence_length = self.pointsGridLayout.itemAtPosition(
                i, 0).widget().text()
            points = self.pointsGridLayout.itemAtPosition(i, 1).widget().text()

            if not points.isnumeric():
                points = "0"
            elif int(points) > int(points_to_win):
                self.resultLabel.setText(
                    "Row: " + str(i) + " Max value = " + points_to_win)
                print("Row: " + str(i) + " Max value = " + points_to_win)
                return [], 0, 0

            sequence_points.append(int(points))

        return sequence_points, int(size), int(points_to_win)
