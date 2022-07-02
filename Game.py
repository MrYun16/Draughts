from Player import Player

class Game:  
    EMPTY = "-"
    def __init__(self, player1, player2):
        self.__player1 = player1
        self.__player2 = player2
        self.__turn = self.__player1
        #self.__board = [[[self.__player1.piece, self.EMPTY][i % 2], [self.__player1.piece, self.EMPTY][(i + 1) % 2]] * 4 for i in range(3)] + [[self.EMPTY] * 8] * 2 + [[[self.__player2.piece, self.EMPTY][(i + 1) % 2], [self.__player2.piece, self.EMPTY][i % 2]] * 4 for i in range(3)] # player1 top (o), player2 bottom (x)
        self.__board = [[self.__player1.piece, self.EMPTY]*4,
        [self.EMPTY, self.__player1.piece]*4,
        [self.__player1.piece, self.EMPTY]*4,
        ] + [[self.EMPTY] * 8 for _ in range(2)] + [[self.__player2.piece, self.EMPTY]*4,
        [self.EMPTY, self.__player2.piece]*4,
        [self.__player2.piece, self.EMPTY]*4]

        for row in self.__board:
            print(row)

    def play(self, x1, y1, x2, y2):
        x1 = x1 - 1
        y1 = y1 - 1
        x2 = x2 - 1
        y2 = y2 - 1

        if self.__board[y1][x1] != self.__turn.piece:
            raise GameError("No piece exists here")
        if abs(x1 - x2) == 1 and y2 - y1 == self.__turn.direction: # one unit move
            self.__board[y1][x1] = self.EMPTY
            self.__board[y2][x2] = self.__turn.piece

            if self.__turn == self.__player1: # error here
                self.__turn = self.__player2
            else:
                self.__turn = self.__player1
            
        elif abs(x1 - x2) == 2 and y2 - y1 == self.__turn.direction * 2 and self.__board[0.5(x1+x2)][0.5(1+y2)] != self.__turn.piece and self.__board[0.5(x1+x2)][0.5(1+y2)] != self.EMPTY: # jumping
            print("Entered 2nd if statement")
            self.__board[y1][x1], self.__board[0.5(x1+x2)][0.5(1+y2)] = self.EMPTY, self.EMPTY
            self._board[y2][x2] = self.__turn.piece
            

            if self.__turn == self.__player1:
                self.__player2.decreaseNumPieces(1)
                self.__turn = self.__player2
            else:
                self.__player1.decreaseNumPieces(1)
                self.__turn = self.__player1
        else:
            raise GameError("Move not possible")




    def getWinner(self):
        if self.__player1.numPieces == 0:
            return self.__player1.name
        elif self.__player2.numPieces == 0:
            return self.__player2.name
        return None

    def __repr__(self):
        result = "  " + " ".join(map(str, list(col for col in range(1, 9))))
        for i, row in enumerate(self.__board):
            result += f"\n{i+1} " + " ".join(row)
        result += f"\n{self.__player1.name}({self.__player1.piece}): {self.__player1.numPieces} {self.__player2.name}({self.__player2.piece}): {self.__player2.numPieces}"
        result += f"\n{self.__turn.name}'s turn (enter coordinates for starting then ending square for moving piece e.g. x1 y1 x2 y2"
        return result

class GameError(Exception):
    pass

