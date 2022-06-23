from Player import Player

class Game:  
    P1 = "o"
    P2 = "x"
    EMPTY = "-"
    def __init__(self, player1, player2):
        self.__player1 = player1
        self.__player2 = player2
        self.__turn = self.__player1
        self.__board = [[[self.P1, self.EMPTY][i % 2], [self.P1, self.EMPTY][(i + 1) % 2]] * 4 for i in range(3)] + [[self.EMPTY] * 8] * 2 + [[[self.P2, self.EMPTY][(i + 1) % 2], [self.P2, self.EMPTY][i % 2]] * 4 for i in range(3)]

    

    def getWinner(self):
        if self.__player1.numPieces == 0:
            return self.__player1.name
        elif self.__player2.numPieces == 0:
            return self.__player2.name
        return None

    def __repr__(self):
        result = " " + " ".join(map(str, list(col for col in range(1, 9))))
        for i, row in enumerate(self.__board):
            result += f"\n{i+1} " + " ".join(row)
        result += f"\n{self.__player1.name}: {self.__player1.numPieces} {self.__player2.name}: {self.__player1.numPieces}"
        result += f"\n{self.__turn.name}'s turn"
        return result


a = Game(Player("Joe"), Player("Hart"))
print(a)