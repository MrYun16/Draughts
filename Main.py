from Ui import Gui, Terminal
from sys import argv
from Game import Game
from Player import Player


if __name__ == "__main__":
    if len(argv) == 1:
        ui = Terminal(Game(Player("Joe", "o"), Player("Daniel", "x")))
    ui.run()