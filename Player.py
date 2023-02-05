from abc import abstractmethod
from Piece import Piece
from random import *
from clock import *
from threading import *
from time import *
from tkinter import *
from copy import deepcopy

class Player:
    def __init__(self, name, colour, direction, boardLen) -> None:
        self.__numPieces = int((boardLen-2)*boardLen/4) # left
        self.__name = name
        self.__direction = direction # 1 is down - so player one
        self.__colour = colour
        self.__isAI = False
        self.__timeBeforeSaved = None # in demi sec


    @property
    def timeBeforeSaved(self):
        return self.__timeBeforeSaved

    ##########################################################
    # CATEGORY A ALGORITHMS: COMPLEX OOP - ASSOCIATION
    # Creats a Clock object for Player defined with the Player
    # class - composition
    # CATEGORY B ALGORITHMS: GENERATION OF OBJECTS USING OOP
    ##########################################################
    def createClock(self, startTime, clockDisplayString, win):
        self.clock = Clock(startTime, clockDisplayString, win)

    def deleteClock(self): # also saves the time into the player
        self.__timeBeforeSaved = self.clock.currentTimeInDemiSec
        del self.clock

    def changIsAI(self, new):
        self.__isAI = new

    def amendTimeBeforeSaved(self, t):
        self.__timeBeforeSaved = t

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
    def __init__(self, name, colour, direction, boardLen) -> None:
        super().__init__(name, colour, direction, boardLen)
        self.changIsAI(True)

    def _getPossiblePiecesToMoveWithDestination(self, game): # in the format ls = [piece.x, piece.y, toCoord[0], toCoord[1]]
        possiblePlays = []
        ownPieces = game.getOwnPieces()
        if game.jumpingPiece != None: # in jumping spree
            piece = game.jumpingPiece
            for toCoord in game.getSqrsToJumpTo(piece):

        #################################################################
        # CATEGORY A ALGORITHMS: LIST OPERATIONS
        # In the following three for loops, a list element is appended to 
        # possiblePlays
        #################################################################
                possiblePlays.append([piece.x+1, piece.y+1, toCoord[0]+1, toCoord[1]+1])

        elif game.playerCanJump():
            for piece in ownPieces:
                if len(game.getSqrsToJumpTo(piece)) > 0:
                    for toCoord in game.getSqrsToJumpTo(piece):
                        possiblePlays.append([piece.x+1, piece.y+1, toCoord[0]+1, toCoord[1]+1])
        else:
            for piece in ownPieces:
                if len(game.getSqrsToWalkTo(piece)) > 0:
                    for toCoord in game.getSqrsToWalkTo(piece):
                        possiblePlays.append([piece.x+1, piece.y+1, toCoord[0]+1, toCoord[1]+1])
        return possiblePlays


    def _evaluate(self, game, player): # only checking difference in material so far
        res = 0
        board = game.board
        for row in board[:]:
            for piece in row:
                if piece != game.EMPTY:
                    if piece.belongsToPlayer(player):
                        res += 1
                    else:
                        res -= 1
        return res

    #####################################################################
    # CATEGORY A MODEL: COMPLEX USER-DEFINED USE OF OOP - ABSTRACT METHOD
    #####################################################################
    @abstractmethod
    def findMove(self, game):
        pass



################################################################
# CATEGORY A MODEL: COMPLEX USER-DEFINED USE OF OOP - INHERITANCE
# the easy and hard AIs (randomAI and hardAI) are derived from 
# the AI class, which is also derived from the Player Class
################################################################
class randomAI(AI):
    def __init__(self, name, colour, direction, boardLen) -> None:
        super().__init__(name, colour, direction, boardLen)


    ##########################################
    # CATEGORY A MODEL: COMPLEX OOP
    # Polymorphism - different implementations 
    # for findMove between randomAI and the 
    # following hardAI
    ##########################################
    def findMove(self, game):
        return choice(self._getPossiblePiecesToMoveWithDestination(game))

class hardAI(AI):
    PLAY = 1
    GAME = 0
    EVALUATEDVALUE = 0
    def __init__(self, name, colour, direction, boardLen) -> None:
        super().__init__(name, colour, direction, boardLen)

    def findMove(self, game):
        chosenPlay = self.__minimax(3, game, None, game.currentPlayer)[self.PLAY]
    
        return chosenPlay

    #######################################################################
    # CATEGORY A ALGORITHM: Recursive Algorithms
    # Using recursion to generate next game state of a tree for the minimax
    ######################################################################
    def __minimax(self, depth, game, prevPlay, maxingPlayer):
        if depth == 0:
            return [self._evaluate(game, maxingPlayer), prevPlay]
        nodesValues =  [[self.__minimax(depth-1, node[self.GAME], node[self.PLAY], maxingPlayer),node[self.PLAY]] for node in self.__getNextNodes(game)] # minimax returns [evaluatedValue, playIntoThatGameState], node is [gameState, playIntoThatGameState]and nodesValues contains list of [minimax, node]
        nodesValues = self._sort(nodesValues)
        
        if maxingPlayer == game.currentPlayer: # maximising
            return [nodesValues[-1][self.EVALUATEDVALUE], nodesValues[-1][self.PLAY]]
        else: # minimising
            return [nodesValues[0][self.EVALUATEDVALUE], nodesValues[0][self.PLAY]]

    ######################################
    # CATEGORY A ALGORITHMS: MERGE SORT
    # To sort nodeValues, I used mergesort
    ######################################
    def _sort(self, nodesValues):
        if len(nodesValues) == 1:
            return nodesValues
        nV1, nV2 = nodesValues[:len(nodesValues)//2], nodesValues[len(nodesValues)//2:]
        nV1, nV2 = self._sort(nV1), self._sort(nV2)
        ls = []
        while len(nV1) and len(nV2):
            if nV1[0][1][self.EVALUATEDVALUE] < nV2[0][1][self.EVALUATEDVALUE]:
                ls.append(nV1[0])
                del nV1[0]
            else:
                ls.append(nV2[0])
                del nV2[0]

        ########################################
        # CATEGORY A ALGORITHMS: LIST OPERATIONS
        # Here, used extend() list operation
        ########################################
        ls.extend(nV1)
        ls.extend(nV2)
        return ls

    def __getNextNodes(self, game):
        possiblePlays = self._getPossiblePiecesToMoveWithDestination(game)
        nextNodes = []
        for play in possiblePlays:
            newGame = deepcopy(game)
            newGame.play(*play) # check this extraction works

            ########################################
            # CATEGORY A ALGORITHMS: LIST OPERATIONS
            # Here, used append() list operation
            ########################################
            nextNodes.append([newGame, play])
 
        return nextNodes