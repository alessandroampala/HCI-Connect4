class Board:
    #Constructor for the Board object
    def _init_(self, size, max_point):
        self._size=size
        self._max_point=max_point

    #Get size of the board
    def get_size(self):
        return self.size
    
    #Get how many points a player need to finish a game
    def get_max_points(self):
        return self.max_point