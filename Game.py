from Piece import Stone, King
from Player import Player

class Game:  
    EMPTY = "-"
    VECTS = [[-2, -2], [-2, 2], [2, -2], [2, 2]]
    def __init__(self, player1, player2):
        self.__player1 = player1
        self.__player2 = player2
        self.__currentPlayer = self.__player1
        self.__jumpingPiece = None # piece that must keeping jumping if possible
        #self.__board = [[[self.__player1.piece, self.EMPTY][i % 2], [self.__player1.piece, self.EMPTY][(i + 1) % 2]] * 4 for i in range(3)] + [[self.EMPTY] * 8] * 2 + [[[self.__player2.piece, self.EMPTY][(i + 1) % 2], [self.__player2.piece, self.EMPTY][i % 2]] * 4 for i in range(3)] # player1 top (o), player2 bottom (x)
        
        self.__board = [[self.EMPTY for _ in range(8)] for _ in range(8)]
        self.prepareBoard()
        """
        self.__board = [[self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, Stone("white", True, 1, 4, 0), self.EMPTY, self.EMPTY, self.EMPTY],
        [self.EMPTY, self.EMPTY, Stone("white", True, 1, 2, 1), self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, ],
        [self.EMPTY, Stone("black", False, -1, 1, 2), self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, ],
        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, ],
        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, ],
        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, ],
        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, ],
        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, ]]
        """

    @property
    def board(self):
        return self.__board

    def prepareBoard(self): # self, colour, direction, x, y
        for col in range(0, 8, 2):
            self.__board[0][col] = Stone("white", 1, col, 0)
        for col in range(1, 8, 2):
            self.__board[1][col] = Stone("white", 1, col, 1)
        for col in range(0, 8, 2):
            self.__board[2][col] = Stone("white", 1, col, 2)
        
        for col in range(1, 8, 2):
            self.__board[5][col] = Stone("black", -1, col, 5)
        for col in range(0, 8, 2):
            self.__board[6][col] = Stone("black", -1, col, 6)
        for col in range(1, 8, 2):
            self.__board[7][col] = Stone("black", -1, col, 7)
        
    def ownPiece(self, x, y): # accounts for empty sqr
        x -= 1
        y -= 1

        currentPiece = self.__board[y][x] 
        #print(x, y, currentPiece, currentPiece.colour, self.__currentPlayer.colour)
        if currentPiece == self.EMPTY:
            raise GameError("No piece exists here")
        elif currentPiece.colour != self.__currentPlayer.colour:
            raise GameError("Not your piece")  

    def vacantSquare(self, x, y):
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
                raise GameError("Must move same piece as it can jump again")
            elif self.isJump(currentPiece, x2, y2):
                self.jump(currentPiece, x2, y2)
                if self.canJump(self.__board[y2][x2]):
                    self.__jumpingPiece = self.canJump(self.__board[y2][x2])
                else:
                    self.__jumpingPiece = None
            else:
                raise GameError("Not possible")
        elif self.__jumpingPiece == None: # actual moving/jumping sequences - not in jumping spree
            if self.playerCanJump():
               
                if self.isMove(currentPiece, x2, y2):
                    raise GameError("Jump is possible")
                elif self.isJump(currentPiece, x2, y2):
                    self.jump(currentPiece, x2, y2)
                    if self.canJump(currentPiece):
                        
                        self.__jumpingPiece = currentPiece # entering jumping loop
                else:
                    raise GameError("Move not possible")
            else:
                if self.isMove(currentPiece, x2, y2):
                    self.move(currentPiece, x2, y2)
                    self.__jumpingPiece = None
                else:
                    raise GameError("Move not possible")

        
        if not self.__jumpingPiece: # it exists
            self.switchTurn()

        if (y2 == 0 or y2 == 7) and self.__board[y2][x2].isStone:
            self.__board[y2][x2] = self.__board[y2][x2].promoted()
            if self.__jumpingPiece != None: # was on a jumping streak
                self.__jumpingPiece = None # end the streak
                self.switchTurn()
       
    def playerCanJump(self):
        if self.__currentPlayer.direction == 1:
          
            for y in range(8):
                for x in range(8):
                    piece = self.__board[y][x]
                    if piece != self.EMPTY and piece.direction == self.__currentPlayer.direction:
                        if self.canJump(piece):
                            return True
        else:
            for y in range(7, -1, -1):
                for x in range(8):
                    piece = self.__board[y][x]
                    if piece != self.EMPTY:
                        if self.canJump(piece):
                            return True
        return False
    

    def canJump(self, currentPiece):
        for vect in currentPiece.vectors: # [[2, -2], [2, 2]] for direction 1
            x2 = currentPiece.x + vect[1]
            y2 = currentPiece.y + vect[0]
            if x2 in range(8) and y2 in range(8):
                if self.isJump(currentPiece, x2, y2):
                    return True
        return False

    def isJump(self, currentPiece, x2, y2): 
        if min([currentPiece.x, currentPiece.y, x2, y2]) < 0 or max([currentPiece.x, currentPiece.y, x2, y2]) >= 8:
            return False
        dx, dy = x2 - currentPiece.x, y2 - currentPiece.y
        if currentPiece.isStone:
            
            if abs(dx) == 2 and dy == self.__currentPlayer.direction * 2 and self.__board[int(0.5*(currentPiece.y+y2))][int(0.5*(currentPiece.x+x2))] != self.EMPTY and self.__board[int(0.5*(currentPiece.y+y2))][int(0.5*(currentPiece.x+x2))].direction != self.__currentPlayer.direction and self.__board[y2][x2] == self.EMPTY:
                return True
            return False
        else: # is a king
            
            if abs(dx) == 2 and abs(dy) == 2 and self.__board[int(0.5*(currentPiece.y+y2))][int(0.5*(currentPiece.x+x2))] != self.EMPTY and self.__board[int(0.5*(currentPiece.y+y2))][int(0.5*(currentPiece.x+x2))].colour != self.__currentPlayer.colour and self.__board[y2][x2] == self.EMPTY:
                return True
            return False

    def isMove(self, currentPiece, x2, y2):
        if min([currentPiece.x, currentPiece.y, x2, y2]) < 0 or max([currentPiece.x, currentPiece.y, x2, y2]) >= 8:
            return False
        dx, dy = x2 - currentPiece.x, y2 - currentPiece.y
        if currentPiece.isStone:
            if abs(dx) == 1 and dy == self.__currentPlayer.direction: # one unit move, moving square always unoccupied
                return True
            return False
        else:  # is a king
            if abs(dx) == 1 and abs(dy) == 1:
                return True
            return False
  
    def move(self, currentPiece, x2, y2):
        self.__board[y2][x2] = currentPiece
        self.__board[currentPiece.y][currentPiece.x] = self.EMPTY
        currentPiece.updateXY(x2, y2)

    def jump(self, currentPiece, x2, y2):
        x1, y1 = currentPiece.x, currentPiece.y
        self.move(currentPiece, x2, y2)
        self.__board[int(0.5*(y1 + y2))][int(0.5*(x1 + x2))] = self.EMPTY
        if self.__currentPlayer == self.__player1:
            self.__player2.decreaseNumPieces(1)
        else:
            self.__player1.decreaseNumPieces(1)

    def at(self, x, y):
        return str(self.__board[y][x])

    def switchTurn(self):
        if self.__currentPlayer == self.__player1:
            self.__currentPlayer = self.__player2
        else:
            self.__currentPlayer = self.__player1

    def getWinner(self):
        if self.__player1.numPieces == 0:
            return self.__player1.name
        elif self.__player2.numPieces == 0:
            return self.__player2.name
        return None


    def __repr__(self):
        result = "  " + " ".join(map(str, list(col for col in range(1, 9))))
        for i, row in enumerate(self.__board):
            result += f"\n{i+1} " + " ".join(str(x) for x in row)
        result += f"\n{self.__player1.name}({self.__player1.colour}): {self.__player1.numPieces} {self.__player2.name}({self.__player2.colour}): {self.__player2.numPieces}"
        result += f"\n{self.__currentPlayer.name}'s turn (enter coordinates for starting then ending square for moving piece in separate lines e.g. \nx1 y1 \nx2 y2"
        return result
   
class GameError(Exception):
    pass

