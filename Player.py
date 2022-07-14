from Piece import Piece

class Player:
    def __init__(self, name, colour, direction) -> None:
        self.__numPieces = 12 # left
        self.__name = name
        self.__direction = direction # 1 is down - so player one
        self.__colour = colour
        self.__time = 120 # can be changed

    @property
    def numPieces(self):
        return self.__numPieces

    @property
    def time(self):
        return self.__time

    def amendTime(self, t):
        self.__time = t

    @property
    def name(self):
        return self.__name

    @property
    def direction(self):
        return self.__direction

    @property
    def colour(self):
        return self.__colour

    def decreaseNumPieces(self, n): #?
        self.__numPieces -= n