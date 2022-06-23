from Ui import Gui, Terminal
from sys import argv


if __name__ == "__main__":
    if len(argv) == 1:
        ui = Terminal()
    ui.run()