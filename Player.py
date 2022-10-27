from abc import abstractmethod
from Piece import Piece
from random import *
from clock import *
from threading import *
from time import *
from copy import deepcopy

class Player:
    def __init__(self, name, colour, direction) -> None:
        self.__numPieces = 12 # left
        self.__name = name
        self.__direction = direction # 1 is down - so player one
        self.__colour = colour
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

    def createTimer(self, initialTimeInSec, timeString):
       # self.__Timer = Timer(initialTimeInSec, timeString)
        #timeString.set("IN PLAYER")
        new_thread = Thread(target=self.test, args=(timeString,))
        new_thread.start()

    def test(self, string):
        for _ in range(3):
            string.set(f"changed to {_}")
            sleep(1)
            

    def startTimer(self):
        self.__Timer.start()

    def stopTimer(self):
        self.__Timer.cancel()

class AI(Player):
    def __init__(self, name, colour, direction) -> None:
        super().__init__(name, colour, direction)
        self.changIsAI(True)

    def getPossiblePlays(self, game): # in the format ls = [piece.x, piece.y, toCoord[0], toCoord[1]]
        possiblePlays = []
        ownPieces = game.getOwnPieces()
        if game.jumpingPiece != None: # in jumping spree
            piece = game.jumpingPiece
            for toCoord in game.getSqrsToJumpTo(piece):
                possiblePlays.append([piece.x+1, piece.y+1, toCoord[0]+1, toCoord[1]+1])
        elif game.playerCanJump():
            for piece in ownPieces:
                if len(game.getSqrsToJumpTo(piece)) > 0:
                    for toCoord in game.getSqrsToJumpTo(piece):
                        possiblePlays.append([piece.x+1, piece.y+1, toCoord[0]+1, toCoord[1]+1])
        else:
            for piece in ownPieces:
                if len(game.getSqrsToMoveTo(piece)) > 0:
                    for toCoord in game.getSqrsToMoveTo(piece):
                        possiblePlays.append([piece.x+1, piece.y+1, toCoord[0]+1, toCoord[1]+1])
        return possiblePlays


    def evaluate(self, game, player): # only checking difference in material so far
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

    @abstractmethod
    def findMove(self, game):
        pass

class randomAI(AI):
    def __init__(self, name, colour, direction) -> None:
        super().__init__(name, colour, direction)

    def findMove(self, game):
        return choice(self.getPossiblePlays(game))


class hardAI(AI):
    PLAY = 1
    GAME = 0
    def __init__(self, name, colour, direction) -> None:
        super().__init__(name, colour, direction)

    def findMove(self, game):
        print("in the findmove")
        chosenPlay = self.minimax(3, game, None, game.currentPlayer)[1]
        print(chosenPlay)
        return chosenPlay

    def minimax(self, depth, game, prevPlay, maxingPlayer):
        if depth == 0:
            return [self.evaluate(game, maxingPlayer),prevPlay] # node format = [game, play]
        nodesValues =  [[node[self.PLAY], self.minimax(depth-1, node[self.GAME], prevPlay, maxingPlayer)] for node in self.getNextNodes(game)]
       # print(f"depth{depth}: {[node[1] for node in self.getNextNodes(game)]}")
        nodesValues.sort(key=lambda row: (row[0]))
        if maxingPlayer == game.currentPlayer: # maximising
            return [nodesValues[-1][1], nodesValues[-1][0]]
        else: # minimising
            return [nodesValues[0][1], nodesValues[0][0]]

    def getNextNodes(self, game):
        #print("getnextnodes")
        possiblePlays = self.getPossiblePlays(game)
        nextNodes = []
        for play in possiblePlays:
            newGame = deepcopy(game)
            newGame.play(*play) # check this extraction works
            nextNodes.append([newGame, play])
        if len(nextNodes) == 0:
            print("NODES IS 0")
        return nextNodes


"""
class player:
    def init(self, name):
        self.name = name
        self.timer = 0

    def printName(self):
        print(self.name)

    def incrementTimer(self):
        self.timer += 1

    def runTimer(self):
        while True:
            time.sleep(1)
            self.incrementTimer()

    def runTimer(self):
        thread = threading.Thread(target=self.runTimer)
        thread.daemon = True
        thread.start()
"""
        