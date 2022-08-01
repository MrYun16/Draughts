from Ui import Gui, Terminal, Ui
from sys import argv
from Game import Game
from Player import Player


if __name__ == "__main__":
    if len(argv) == 1:
        #ui = Ui(Game(Player("Joe", "white", 1), Player("Daniel", "black", -1)))
        ui = Gui()
    ui.run()
