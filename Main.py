from Ui import Gui, Terminal
from sys import argv
from Game import Game
from Player import Player
from sys import argv


def usage():
    print(f"t for terminal, g for GUI"
    )
    quit()


if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    if argv[1] == "t":
        ui = Terminal()
        ui.run()
    elif argv[1] == "g":
        ui = Gui()
        ui.run()
    else:
        usage()

if __name__ == "__main__":
    if len(argv) == 1:
        ui = Gui()
    ui.run()









































