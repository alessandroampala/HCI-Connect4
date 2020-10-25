from PyQt5 import QtWidgets, QtCore, QtGui, uic
import threading
import time


class GameGui(QtWidgets.QMainWindow):
    def __init__(self, game_round, menu_window):
        # Call the inherited classes __init__ method
        super(GameGui, self).__init__()
        uic.loadUi("res/layout/game.ui", self)  # Load the .ui file

        self.score_row_points = 1

        self.players_round_position = 0

        self.round = game_round

        self.menu_window = menu_window

        self.setWindowIcon(QtGui.QIcon("res/images/unito.png"))

        self.add_board()

        self.showMaximized()

        self.players = self.round.get_players()
        self.show_score()

        self.yourTurnPushButton.setStyleSheet(
            "background-color: " + self.players[self.players_round_position].get_color() + "; border: 2px solid white; border-radius: 20px;")
        self.playerNameLabel.setText(self.players[self.players_round_position].get_name())

        self.show()  # Show the GUI

        self.retryButton.clicked.connect(self.retry_button_pressed)

        self.backButton.clicked.connect(self.back_button_pressed)


    def add_board(self):
        for x in range(15):
            for y in range(15):
                cell_button = QtWidgets.QPushButton()
                cell_button.setStyleSheet(
                    "background-color: white; border: 2px solid white; border-radius: 15px;")
                cell_button.setSizePolicy(
                    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                cell_button.setMaximumSize(40, 40)
                cell_button.setMinimumSize(40, 40)
                cell_button.setCursor(QtGui.QCursor(
                    QtCore.Qt.PointingHandCursor))

                cell_button.clicked.connect(
                    lambda: self.cell_button_pressed(self.sender()))

                self.boardGridLayout.addWidget(cell_button, x, y)

    def cell_button_pressed(self, cell_button):
        cell_button.setStyleSheet(
            "border: 2px solid white; border-radius: 15px; background-color: " + self.yourTurnPushButton.palette().color(
                QtGui.QPalette.Background).name() + ";")
        cell_button.clicked.disconnect()
        cell_button.setCursor(QtGui.QCursor(
            QtCore.Qt.ArrowCursor))

        index = self.boardGridLayout.indexOf(cell_button)
        position = self.boardGridLayout.getItemPosition(index)

        self.round.set_cell(int(position[0]), int(position[1]), self.players[self.players_round_position])

        self.players_round_position = (self.players_round_position + 1) % len(self.players)

        self.yourTurnPushButton.setStyleSheet(
            "background-color: " + self.players[
                self.players_round_position].get_color() + "; border: 2px solid white; border-radius: 20px;")
        self.playerNameLabel.setText(self.players[self.players_round_position].get_name())


    def retry_button_pressed(self):
        self.close()

    def back_button_pressed(self):
        self.menu_window.show()
        self.close()

    def show_score(self):
        for player in self.players:
            player_color = player.get_color()
            player_name = player.get_name()

            color_button = QtWidgets.QPushButton()
            color_button.setStyleSheet(
                "background-color: " + player_color + "; border: 2px solid white; border-radius: 20px;")
            color_button.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            color_button.setMaximumSize(40, 40)
            color_button.setMinimumSize(40, 40)

            name_line_edit = QtWidgets.QLineEdit()
            name_line_edit.setStyleSheet(
                "font-size:10pt")
            name_line_edit.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            name_line_edit.setMaximumHeight(30)
            name_line_edit.setMinimumHeight(30)
            name_line_edit.setText(player_name)
            name_line_edit.setEnabled(False)
            name_line_edit.setAlignment(QtCore.Qt.AlignCenter)

            score_line_edit = QtWidgets.QLineEdit()
            score_line_edit.setStyleSheet(
                "font-size:10pt")
            score_line_edit.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            score_line_edit.setMaximumHeight(30)
            score_line_edit.setMinimumHeight(30)
            score_line_edit.setText(str(player.get_points()))
            score_line_edit.setEnabled(False)
            score_line_edit.setAlignment(QtCore.Qt.AlignCenter)

            self.scoreGridLayout.addWidget(color_button, self.score_row_points, 0)
            self.scoreGridLayout.addWidget(name_line_edit, self.score_row_points, 1)
            self.scoreGridLayout.addWidget(score_line_edit, self.score_row_points, 2)

            self.score_row_points += 1



