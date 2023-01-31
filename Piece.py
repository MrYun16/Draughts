

class Piece:
    def __init__(self, colour, direction, x, y):   
        self.__colour = colour
        self.__direction = direction
        self.__isStone = None
        self.__value = None
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

    def belongsToPlayer(self, player):
        if self.colour == player.colour:
            return True
        return False

    @property
    def direction(self):
        return self.__direction

    @property
    def colour(self):
        return self.__colour

    @property
    def value(self):
        return self.value

    def setValue(self, v):
        self.__value = v

    def changeIsStone(self, value):
        self.__isStone = value

    @property
    def isStone(self):
        return self.__isStone

    def __repr__(self) -> str:
        pass


################################################################
# CATEGORY A MODEL: COMPLEX USER-DEFINED USE OF OOP - INHERITANCE
# following Stone derived from Piece and King derived from Stone
#################################################################

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
        self.setValue(1)
    
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

    ##########################################
    # CATEGORY A MODEL: COMPLEX OOP
    # Polymorphism - different implementations 
    # for __repre__() between Stone and King
    ##########################################
    def __repr__(self) -> str:
        if self.direction == 1:
            return "o"
        return "x"

class King(Piece):

    @property
    def jumpVects(self):
        return self.__jumpVects

    @property
    def moveVects(self):
        return self.__moveVects
        
    def __init__(self, colour, direction, x, y):
        super().__init__(colour, direction, x, y)
        self.changeIsStone(False)
        self.__jumpVects = [[-2, -2], [-2, 2], [2, -2], [2, 2]]
        self.__moveVects = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        self.setValue(3)

    def __repr__(self) -> str:
        if self.direction == 1:
            return "0"
        return "+"

