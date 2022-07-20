from abc import abstractmethod


class Piece:
    def __init__(self, colour, direction, x, y):   
        self.__colour = colour
        self.__direction = direction
        self.__isStone = None
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    def updateXY(self, newX, newY):
        self.__x = newX
        self.__y = newY

    @property
    def direction(self):
        return self.__direction

    @property
    def colour(self):
        return self.__colour

    #@isStone.setter
    def changeIsStone(self, value):
        self.__isStone = value

    @property
    def isStone(self):
        return self.__isStone

    def __repr__(self) -> str:
        pass

class Stone(Piece):
    def __init__(self, colour, direction, x, y):
        super().__init__(colour, direction, x, y)
        self.changeIsStone(True)
        if direction == 1: # down
            self.__jumpVects = [[-2, 2], [2, 2]]
            self.__moveVects = [[-1, 1], [1, 1]]
        else: # up
            self.__jumpVects = [[2, -2], [-2, -2]]
            self.__moveVects = [[1, -1], [-1, -1]]
    
    @property
    def jumpVects(self):
        return self.__jumpVects

    @property
    def moveVects(self):
        return self.__moveVects

    def changeJumpVects(self, new):
        self.__jumpVects = new

    def changeMoveVects(self, new):
        self.__moveVects = new


    def getPromoted(self):
        return King(self.colour, self.direction, self.x, self.y)

    def __repr__(self) -> str:
        if self.direction == 1:
            return "o"
        return "x"

class King(Piece):
    def __init__(self, colour, direction, x, y):
        super().__init__(colour, direction, x, y)
        self.changeIsStone(False)
        self.changeJumpVects([[-2, -2], [-2, 2], [2, -2], [2, 2]])
        self.changeMoveVects([[-1, -1], [-1, 1], [1, -1], [1, 1]])

    def __repr__(self) -> str:
        if self.direction == 1:
            return "0"
        return "+"

