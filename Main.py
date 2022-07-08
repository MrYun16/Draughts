from Ui import Gui, Terminal
from sys import argv
from Game import Game
from Player import Player


if __name__ == "__main__":
    if len(argv) == 1:
        ui = Terminal(Game(Player("Joe", "white", 1, True), Player("Daniel", "black", -1, False)))
    ui.run()
    