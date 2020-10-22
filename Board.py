class Board:
    # Constructor for the Board object
    def __init__(self, size):
        self._size = size
        self._board = []
        # Create empty matrix
        for i in range(self._size):
            self._board.append([])

    # Get size of the board
    def get_size(self):
        return self._size

    # Set the color of a cell
    def set_cell(self, x, y, player):
        self._board[x][y] = player.get_color()
