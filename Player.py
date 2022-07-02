class Player:
    def __init__(self, name, piece) -> None:
        self.__numPieces = 12 # left
        self.__name = name
        self.__piece = piece
        if self.__piece == "o":
            self.__direction = 1
        else:
            self.__direction = -1

    @property
    def numPieces(self):
        return self.__numPieces

    @property
    def name(self):
        return self.__name

    @property
    def piece(self):
        return self.__piece

    @property
    def direction(self):
        return self.__direction

    def decreaseNumPieces(self, n): #?
        self.__numPieces -= n