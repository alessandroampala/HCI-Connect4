class Board:
    # Constructor for the Board object
    def __init__(self, size):
        self._size = size
        self._board = []
        # Create empty matrix
        for i in range(self._size):
            self._board.append([None] * self._size)

    # Get size of the board
    def get_size(self):
        return self._size

    # Set the color of a cell
    def set_cell(self, x, y, color):
        self._board[y][x] = color

    def get_cell(self, x, y):
        return self._board[y][x]

    def debug_print_board(self):
        for i in range(self.get_size()):
            for j in range(self.get_size()):
                if self.get_cell(i, j) is not None:
                    print(self.get_cell(i, j), end="")
                else:
                    print("-", end="")
            print()
