from Game import GameError

class Ui:
    def __init__(self, game):
        self.__game = game

    def getInput(self):
        invalid = True
        while invalid:
            userInput = input().split()
            if len(userInput) != 4:
                print("Invalid input - please try again")
            else:
                [x1, y1, x2, y2] = list(map(int, userInput))
                if min(x1, y1, x2, y2) in range(1, 9) and max(x1, y1, x2, y2) in range(1, 9):
                    break
                else:
                    print("Invalid input - please try again")
        return x1, y1, x2, y2

    def run(self):
        while self.__game.getWinner() == None:
            print(self.__game)
            notPossible = True

            while notPossible:
                x1, y1, x2, y2 = self.getInput()
                try:
                    self.__game.play(x1, y1, x2, y2)
                    notPossible = False
                except GameError as e:
                    print(e)
                    


class Gui(Ui):
    pass

class Terminal(Ui):
    def __init__(self, game):
        super().__init__(game)