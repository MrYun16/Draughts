from abc import abstractmethod


class Piece:
    def __init__(self, colour, direction, x, y):   
        self.__colour = colour
        self.__direction = direction
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
    def type(self):
        return self.__type

    @property
    def colour(self):
        return self.__colour

    def __repr__(self) -> str:
        pass

class Stone(Piece):
    def __init__(self, colour, direction, x, y):
        super().__init__(colour, direction, x, y)
        self.isStone = True
        if direction == 1: # down
            self.vectors = [[2, -2], [2, 2]]
        else: # up
            self.vectors = [[-2, -2], [-2, 2]]
    
    def promoted(self):
        return King(self.colour, self.direction, self.x, self.y)

    def __repr__(self) -> str:
        if self.direction == 1:
            return "o"
        return "x"

class King(Piece):
    def __init__(self, colour, direction, x, y):
        super().__init__(colour, direction, x, y)
        self.isStone = False
        self.vectors = [[-2, -2], [-2, 2], [2, -2], [2, 2]]

    def __repr__(self) -> str:
        if self.direction == 1:
            return "0"
        return "+"

