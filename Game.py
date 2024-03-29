from Piece import Stone, King
from Player import Player
from copy import deepcopy

class Game:  
    EMPTY = " " # smth
    VECTS = [[-2, -2], [-2, 2], [2, -2], [2, 2]]
    def __init__(self, player1, player2, boardLen):
        #############################################
        # CATEGORY A MODEL: COMPLEX OOP - ASSOCIATION
        # The player objects belonging to Game is
        # aggregation
        #############################################
        self.__player1 = player1
        self.__player2 = player2
        self.__boardLen = boardLen
        self.__currentPlayer = self.__player1
        self.__jumpingPiece = None # piece that must keeping jumping if possible
        

        

        #########################
        # CATEGORY A MODEL: STACKS
        # Implemented using python
        # lists
        #########################
        self.__boardHistory = []
        self.__piecesHistory = [] # contains [player1.numpieces, player2.numpieces]
        self.__currentPlayerHistory = [] # uses player's direction
        self.__jumpingPieceHistory = []
        

        self.prepareBoard()
        self.updateHistory()

    def updatePlayer1(self, player):
        self.__player1 = player

    def updatePlayer2(self, player):
        self.__player2 = player
    
    def boardHistoryLen(self):
        return len(self.__boardHistory)

    @property
    def boardLen(self):
        return self.__boardLen

    def prepareBoard(self): # self, colour, direction, x, y
        span = int((self.__boardLen-2)/2)

        ##########################################
        # CATEGORY B MODEL: MULTI-DIMENSIONAL ARRAY
        # This board array is 2 dimensional
        ###########################################
        self.__board = [[self.EMPTY for _ in range(self.boardLen)] for _ in range(self.boardLen)]
       
        ######################################################
        #CATEGORY A ALGORITHMS: GENERATION OF OBJECTS USING OOP
        #######################################################
        for i in range(span*self.__boardLen):
            row, col = i//self.__boardLen, i%self.__boardLen
            if (row+i+1)%2:
                self.__board[row][col] = Stone("black", 1, col, row)
        for i in range(span*self.__boardLen):
            row, col = self.__boardLen-span + i//self.__boardLen, i%self.__boardLen
            if (row+i+1)%2:
                self.__board[row][col] = Stone("white", -1, col, row)

  
                
    @property
    def currentPlayer(self):
        return self.__currentPlayer

    def nonCurrentPlayer(self):
        if self.currentPlayer == self.__player1:
            return self.__player2
        return self.__player1

    @property
    def jumpingPiece(self):
        return self.__jumpingPiece

    @property
    def currentPlayer(self):
        return self.__currentPlayer

    @property
    def board(self):
        return self.__board

    def undo(self):
        if len(self.__piecesHistory) == 1:
            raise GameError("Nothing to undo")

        ######################################
        #CATEGORY A ALGORITHM: STACK OPERATIONS
        #######################################
        self.__boardHistory.pop()
        self.__piecesHistory.pop()
        self.__jumpingPieceHistory.pop()
        self.__currentPlayerHistory.pop()
        self.__justUndoed = True
        
        self.__board = deepcopy(self.__boardHistory[-1])
        self.__player1.amendNumPieces(self.__piecesHistory[-1][0])
        self.__player2.amendNumPieces(self.__piecesHistory[-1][1])
        self.__jumpingPiece = self.__jumpingPieceHistory[-1]
        self.__currentPlayer = self.__player1 if self.__currentPlayerHistory[-1] == 1 else self.__player2

    def updateHistory(self):
        #######################################
        #CATEGORY A ALGORITHM: STACK OPERATIONS
        #######################################
        self.__boardHistory.append(deepcopy(self.__board))
        self.__piecesHistory.append([self.__player1.numPieces, self.__player2.numPieces])
        self.__jumpingPieceHistory.append(self.__jumpingPiece)
        self.__currentPlayerHistory.append(1 if self.__currentPlayer.colour == self.__player1.colour else -1)
        
    def checkIsOwnPiece(self, x, y): # accounts for empty sqr, 1 indexed
        x -= 1
        y -= 1

        currentPiece = self.__board[y][x] 
        if currentPiece == self.EMPTY:
            raise GameError("No piece exists here")
        elif currentPiece.colour != self.__currentPlayer.colour:
            raise GameError("Not your piece")  


    ###################################################
    # CATEGORY C MODEL: SINGLE-DIMENSIONAL ARRAY
    # Following function returns a list of object Piece
    ###################################################
    def getOwnPieces(self):
        pieces = []
        for y in range(self.boardLen):
            for x in range(self.boardLen):
                try:
                    self.checkIsOwnPiece(x+1, y+1)
                    pieces.append(self.__board[y][x])
                except:
                    pass
        return pieces


    def checkIsVacant(self, x, y):
        x -= 1
        y -= 1
        if self.__board[y][x] != self.EMPTY:
            raise GameError("Square occupied")



    def play(self, x1, y1, x2, y2): # accepts 1 indexed
        x1 = x1 - 1
        y1 = y1 - 1
        x2 = x2 - 1
        y2 = y2 - 1

        currentPiece = self.__board[y1][x1] 
       

        if self.__jumpingPiece != None: # this is when player is in jumping spree loop
            if self.__jumpingPiece != currentPiece:
                raise GameError("1.Must move same piece as it can jump again")
            elif self.isJump(currentPiece, x2, y2):
                self.jump(currentPiece, x2, y2)
                if self.canJump(self.__board[y2][x2]):
                    self.__jumpingPiece = self.__board[y2][x2]
                else:
                    self.__jumpingPiece = None
            else:
                raise GameError("2.Not possible")
        elif self.__jumpingPiece == None: # actual moving/jumping sequences - not in jumping spree
            if self.playerCanJump():
               
                if self.isWalk(currentPiece, x2, y2):
                    raise GameError("3.Jump is possible")
                elif self.isJump(currentPiece, x2, y2):
                    self.jump(currentPiece, x2, y2)
                    if self.canJump(currentPiece):
                        self.__jumpingPiece = currentPiece # entering jumping loop
                else:
                    raise GameError("4.Move not possible")
            else:
                if self.isWalk(currentPiece, x2, y2):
                    self.walk(currentPiece, x2, y2)
                    self.__jumpingPiece = None
                else:
                    raise GameError("5.Move not possible")

        
        if not self.__jumpingPiece: # it exists
            self.switchTurn()

        if (y2 == 0 or y2 == self.boardLen-1) and self.__board[y2][x2].isStone:
            self.__board[y2][x2] = self.__board[y2][x2].getPromoted()
            if self.__jumpingPiece != None: # was on a jumping streak
                self.__jumpingPiece = None # end the streak
                self.switchTurn()
       
        self.updateHistory()

    def playerCanJump(self):
        for y in range(self.boardLen):
            for x in range(self.boardLen):
                piece = self.__board[y][x]
                if piece != self.EMPTY and piece.colour == self.__currentPlayer.colour:
                    if self.canJump(piece):
                        return True
        return False
    

    def canJump(self, currentPiece):
        if len(self.getSqrsToJumpTo(currentPiece)) > 0:
            return True
        return False

    def isJump(self, currentPiece, x2, y2): 
        if [x2, y2] in self.getSqrsToJumpTo(currentPiece):
            return True
        return False

    def isWalk(self, currentPiece, x2, y2):
        if [x2, y2] in self.getSqrsToWalkTo(currentPiece):
            return True
        return False


    def walk(self, currentPiece, x2, y2):

        ##############################################
        # CATEGORY A ALGORITHMS: LIST OPERATIONS
        # In this case, specific element of 2D arrays is
        # accessed and amended
        ###############################################
        self.__board[y2][x2] = currentPiece
        self.__board[currentPiece.y][currentPiece.x] = self.EMPTY
        currentPiece.updateXY(x2, y2)

    def jump(self, currentPiece, x2, y2):
        x1, y1 = currentPiece.x, currentPiece.y
        self.walk(currentPiece, x2, y2)

        ####################################################
        # CATEGORY C MODEL: SIMPLE MATHEMATICAL CALCULATIONS
        # Following finds middle square between two squares
        ####################################################
        self.__board[int(0.5*(y1 + y2))][int(0.5*(x1 + x2))] = self.EMPTY
        if self.__currentPlayer == self.__player1:
            self.__player2.amendNumPieces(self.__player2.numPieces-1)
        else:
            self.__player1.amendNumPieces(self.__player1.numPieces-1)

    def at(self, x, y):
        return str(self.__board[y][x])

    def switchTurn(self):
        if not self.__player2.isAI:
            if self.__currentPlayer == self.__player1:
                try:
                    self.__player1.clock.stop()
                    self.__player2.clock.start()
                except:
                    pass
                self.__currentPlayer = self.__player2
            else:
                try:
                    self.__player2.clock.stop()
                    self.__player1.clock.start()
                except:
                    pass
                self.__currentPlayer = self.__player1
        else:
           
            if self.__currentPlayer == self.__player1:
                self.__currentPlayer = self.__player2
            else:
                self.__currentPlayer = self.__player1
           
         

    def getWinner(self):
        if self.__player1.numPieces == 0:
            return self.__player2.name
        elif self.__player2.numPieces == 0:
            return self.__player1.name
        return None


    ###########################################
    # CATEGORY B MODEL: MULTI-DIMENSIONAL ARRAY
    # returns a list of lists, which represent
    # vectors of where the piece can arrive 
    # using the vectors
    # within the board but disregarding
    # surrounding pieces
    ###########################################
    def nextCoordsViaVectors(self, piece, vectors): #ensures coords are empty and in range
        coords = []
        for vect in vectors:
        
            x2 = piece.x + vect[0]
            y2 = piece.y + vect[1]
        
            if x2 in range(self.boardLen) and y2 in range(self.boardLen) and self.__board[y2][x2] == self.EMPTY:
                coords.append([x2,y2])
        return coords


    ###########################################
    # CATEGORY B MODEL: MULTI-DIMENSIONAL ARRAY
    # returns a list of lists, which represent
    # vectors of where the piece can arrive 
    # using the vectors
    # within the board and regarding surrounding
    # pieces
    ###########################################
    def getSqrsToJumpTo(self, piece): # return coords
        temp = self.nextCoordsViaVectors(piece, piece.jumpVects)
        coords = []
        for coord in temp:
            middlePiece = self.__board[int((coord[1]+piece.y)/2)][int((coord[0]+piece.x)/2)]
            if middlePiece != self.EMPTY and middlePiece.colour != self.__currentPlayer.colour:
                coords.append(coord)

        return coords

    def getSqrsToWalkTo(self, piece):
        return self.nextCoordsViaVectors(piece, piece.walkVects)

    def __str__(self):
        result = "  " + " ".join(map(str, list(col for col in range(1, self.__boardLen+1))))
        for i, row in enumerate(self.__board):
            result += f"\n{i+1} " + " ".join(str(x) for x in row)

        dirToWord = {1:"downwards",-1:"upwards"}

        result += f"\n{self.__player1.name}({dirToWord[self.__player1.direction]}): {self.__player1.numPieces} {self.__player2.name}({dirToWord[self.__player2.direction]}): {self.__player2.numPieces}"
        result += f"\n{self.__currentPlayer.name}'s turn (enter coordinates for starting then ending square for moving piece in separate lines e.g. \nx1 y1 \nx2 y2"
        return result
   
class GameError(Exception):
    pass

class TimeError(Exception):
    pass