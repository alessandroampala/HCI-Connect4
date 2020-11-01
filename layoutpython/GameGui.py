from PyQt5 import QtWidgets, QtCore, QtGui, uic


class GameGui(QtWidgets.QMainWindow):
    # Constructor for the game
    # game_round -> all the informations needed to start the game
    # menu_window -> the hidden main menu, needed if you want to go back
    def __init__(self, game_round, menu_window):
        self._score_row_points = 1
        self._players_round_position = 0
        self._round = game_round
        self._menu_window = menu_window
        self._players = self._round.get_players()

        super(GameGui, self).__init__()
        uic.loadUi("res/layout/game.ui", self)
        self.setWindowTitle("Game")
        self.setWindowIcon(QtGui.QIcon("res/images/unito.png"))
        self.showMaximized()
        self.show()

        self.add_board()
        self.show_score()

        self.backButton.clicked.connect(self.back_button_pressed)

    @staticmethod
    # Generates a dynamic size
    # a ->  min size
    # b -> max size
    # c -> size chosen by the players divided by the max value of N (NxN)
    def lerp(a, b, c):
        return (c * a) + ((1 - c) * b)

    # Generates the cells for the board, connects them to the handler and chooses the first player
    def add_board(self):
        size = self.lerp(40, 110, self._round.get_size() / 15)
        for x in range(self._round.get_size()):
            for y in range(self._round.get_size()):
                cell_button = QtWidgets.QPushButton()
                cell_button.setStyleSheet(
                    "background-color: white; border: 2px solid white; border-radius: 15px;")
                cell_button.setSizePolicy(
                    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                cell_button.setMaximumSize(size, size)
                cell_button.setMinimumSize(size, size)
                cell_button.setCursor(QtGui.QCursor(
                    QtCore.Qt.PointingHandCursor))

                cell_button.clicked.connect(
                    lambda: self.cell_button_pressed(self.sender()))

                self.boardGridLayout.addWidget(cell_button, x, y)

        self.yourTurnPushButton.setStyleSheet(
            "background-color: " + self._players[
                self._players_round_position].get_color() + "; border: 2px solid white; border-radius: 20px;")
        self.playerNameLabel.setText(self._players[self._players_round_position].get_name())

    # Handles the cell clicked by a player
    # cell_button -> object of the cell clicked by the player
    def cell_button_pressed(self, cell_button):
        cell_button.setStyleSheet(
            "border: 2px solid white; border-radius: 15px; background-color: "
            + self.yourTurnPushButton.palette().color(QtGui.QPalette.Background).name() + ";")
        cell_button.setEnabled(False)
        cell_button.setCursor(QtGui.QCursor(
            QtCore.Qt.ArrowCursor))

        index = self.boardGridLayout.indexOf(cell_button)
        position = self.boardGridLayout.getItemPosition(index)

        self._round.set_cell(int(position[0]), int(position[1]), self._players[self._players_round_position])

        self.scoreGridLayout.itemAtPosition(self._players_round_position + 1, 2).widget().setText(
            str(self._players[self._players_round_position].get_points()))

        self._players_round_position = (self._players_round_position + 1) % len(self._players)

        if self._round.game_ended():
            self.show_winner()

        self.yourTurnPushButton.setStyleSheet(
            "background-color: " + self._players[
                self._players_round_position].get_color() + "; border: 2px solid white; border-radius: 20px;")
        self.playerNameLabel.setText(self._players[self._players_round_position].get_name())

    # Shows the winner of the game and hide the board
    def show_winner(self):
        self.hideGame.hide()
        self.scoreScrollArea.setMaximumWidth(16777215)
        self.backButton.setMaximumWidth(16777215)

        winner_name = self._round.get_winner()
        for row in range(1, len(self._players) + 1):
            item_name = self.scoreGridLayout.itemAtPosition(row, 1)
            item_score = self.scoreGridLayout.itemAtPosition(row, 2)
            if winner_name is None or item_name.widget().text() == winner_name.get_name():
                item_name.widget().setStyleSheet("font-size:10pt; color:white; background-color: lightgreen")
                item_score.widget().setStyleSheet("font-size:10pt; color:white;background-color: lightgreen")
            else:
                item_name.widget().setStyleSheet("font-size:10pt; color:white;background-color: tomato")
                item_score.widget().setStyleSheet("font-size:10pt; color:white;background-color: tomato")

    # Returns to the main menu
    def back_button_pressed(self):
        self._menu_window.show()
        self.close()

    # Generates the score table
    def show_score(self):
        for player in self._players:
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

            self.scoreGridLayout.addWidget(color_button, self._score_row_points, 0)
            self.scoreGridLayout.addWidget(name_line_edit, self._score_row_points, 1)
            self.scoreGridLayout.addWidget(score_line_edit, self._score_row_points, 2)

            self._score_row_points += 1
