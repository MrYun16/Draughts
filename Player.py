class Player:
    def __init__(self, name) -> None:
        self.__numPieces = 12
        self.__name = name

    @property
    def numPieces(self):
        return self.__numPieces

    def decreaseNumPieces(self, n): #?
        self.__numPieces -= n

    @property
    def name(self):
        return self.__name