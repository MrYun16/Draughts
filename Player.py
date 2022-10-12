from Piece import Piece
from random import *

class Player:
    def __init__(self, name, colour, direction) -> None:
        self.__numPieces = 12 # left
        self.__name = name
        self.__direction = direction # 1 is down - so player one
        self.__colour = colour
        self.__time = 120 # can be changed
        self.__isAI = False

    def changIsAI(self, new):
        self.__isAI = new

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
    def isAI(self):
        return self.__isAI

    @property
    def colour(self):
        return self.__colour

    def amendNumPieces(self, n): #?
        self.__numPieces = n

class AI(Player):
    def __init__(self, name, colour, direction) -> None:
        super().__init__(name, colour, direction)
        self.__isAI = True

    def __play(self, game):
        raise NotImplementedError

class randomAI(AI):
    def __init__(self, name, colour, direction) -> None:
        super().__init__(name, colour, direction)
        self.changIsAI(True)

    def findMove(self, game):
        if game.jumpingPiece != None: # in jumping spree
            piece = game.jumpingPiece
            nextCoord = choice(game.getSqrsToJumpTo(piece))
            return [piece.x, piece.y, nextCoord[0], nextCoord[1]]
        elif game.playerCanJump():
            ownPieces = shuffle(game.getOwnPieces())
            for piece in ownPieces:
                if len(game.getSqrsToJumpTo(piece)) > 0:
                #nextCoord = choice(game.getSqrsToJumpTo(piece)
                    nextCoord = choice(game.getSqrsToJumpTo(piece))
                    return [piece.x, piece.y, nextCoord[0], nextCoord[1]]
        else:
            ownPieces = game.getOwnPieces()
            print(ownPieces[0].moveVects)
            notFound = True
            i = 0
            print("own pieces", ownPieces)
            while notFound and i < 20:
                piece = choice(ownPieces) 
                if len(game.getSqrsToMoveTo(piece)) > 0:
                    nextCoord = choice(game.getSqrsToMoveTo(piece))
                    #print([piece.x, piece.y, nextCoord[0], nextCoord[1]], type(piece.x))
                    return [piece.x, piece.y, nextCoord[0], nextCoord[1]]
                i += 1
            return [1, 5, 2, 6]
                    


                

        