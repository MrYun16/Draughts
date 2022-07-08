from Piece import Piece

class Player:
    def __init__(self, name, colour, direction, belongsToPlayerOne) -> None:
        self.__numPieces = 12 # left
        self.__name = name
        self.__direction = direction # 1 is down - so player one
        self.__colour = colour
        self.__belongsToPlayerOne = belongsToPlayerOne
        

    @property
    def numPieces(self):
        return self.__numPieces

    @property
    def name(self):
        return self.__name

    @property
    def direction(self):
        return self.__direction

    @property
    def colour(self):
        return self.__colour

    @property
    def belongsToPlayerOne(self):
        return self.__belongsToPlayerOne

    def decreaseNumPieces(self, n): #?
        self.__numPieces -= n