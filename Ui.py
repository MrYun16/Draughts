from msilib.schema import Font
from Game import GameError, Game
from tkinter import *
from Player import Player, randomAI
from itertools import product
from Database import dbInterface
from tkmacosx import ColorVar

class Ui:
    def __init__(self, game):
        self.__game = game

    def getInput(self):
        invalid = True
        while invalid:
            userInput = input().split()
            if len(userInput) != 2:
                print("Invalid input - please try again")
            else:
                [x, y] = list(map(int, userInput))
                if min(x, y) in range(1, 9) and max(x, y) in range(1, 9):
                    break
                else:
                    print("Invalid input - please try again")
        return (x, y)

    def run(self):
        while self.__game.getWinner() == None:
            print(self.__game)
            notPossible = True

            while notPossible:
                x1, y1 = self.getInput()
                try:
                    self.__game.checkIsOwnPiece(x1, y1)
                except GameError as e:
                    print(e)
                x2, y2 = self.getInput()
                try:
                    self.__game.checkIsVacant(x2, y2)
                except GameError as e:
                    print(e)

                try:
                    self.__game.play(x1, y1, x2, y2)
                    notPossible = False
                except GameError as e:
                    print(e)
                    


class Gui:
    def __init__(self):
        root = Tk()
        root.title("Tic Tac Toe")
        frame = Frame(root)
        frame.pack()
        self.__root = root
        self.__square1col = "white"
        self.__square2col = "red"
        self.__gameOnGoing = False
        self.__dbInterface = dbInterface("database.db")
        self.__login()
        self.__name = "MrYun" # string
        self.__loggedIn = True # needs to be False
        self.__timer = True # False for default

        #Label(frame, textvariable=f"welcome {self.__name}").pack()
        menuHeader = StringVar()
        menuHeader.set(f"welcome {self.__name}")
        Label(frame, textvariable=menuHeader).pack()
        #self.__name.set("MrYun") # only for testing
        
        Button(
            frame,
            text="1 Player",
            command=self.__onePlayer # name of function, not calling function so no brackets
        ).pack(fill=X)  # expands button across horizontally 

        
        Button(
            frame,
            text="2 Player",
            command=self.__twoPlayer
        ).pack(fill=X) 

        Button(
            frame,
            text="Statistics",
            command=self.__statistics
        ).pack(fill=X) 

        Button(
            frame,
            text="Settings",
            command=self.__settings 
        ).pack(fill=X) 

        Button(
            frame,
            text="Quit",
            command=self.__quit 
        ).pack(fill=X) 

    def __login(self): # bad code
        loginWindow = Toplevel(self.__root)
        self.__username = Entry(loginWindow, width=50) # ???
        self.__password = Entry(loginWindow, width=50) # ???


        self.__username.grid(row=0, column=0)
        Label(loginWindow, text="Username").grid(row=0, column=1)
        self.__password.grid(row=1, column=0)
        Label(loginWindow, text="Password").grid(row=1, column=1)
        
        Button(loginWindow, text="Submit", command = self.__handleAccountInput).grid(row=3)

    def __handleAccountInput(self):
        if self.__dbInterface.loginValid(self.__username.get(), self.__password.get()):
            self.__name = self.__username.get()
            self.__loggedIn = True
        else:
            print("no")
            return
        

    def __AImenu(self):
        if self.__gameOnGoing:
            return
        AIwindow = Toplevel(self.__root)
        AIwindow.title("AI difficulty")

        clickedEasy=lambda: self.__playWindow(Player(str(self.__name.get()), "white", 1), randomAI("Player2", "black", -1), "Two Player")

        lvlsFrame = Frame(AIwindow)
        Button(lvlsFrame, text="Easy", command = clickedEasy, pady=20).grid(row=0,column=0)
        Button(lvlsFrame, text="Hard", pady=20).grid(row=1,column=0)
        lvlsFrame.pack()
    
    def __onePlayer(self):
        if self.__gameOnGoing or not self.__loggedIn:
            return
        self.__AImenu()

    def __twoPlayer(self):
        if self.__gameOnGoing or not self.__loggedIn:
            return
        self.__playWindow(Player(self.__name, "white", 1), Player("Player2", "black", -1), "Two Player")
        self.__gameOnGoing = True

    def __statistics(self):
        if self.__gameOnGoing or not self.__loggedIn:
            return
        statsWindow = Toplevel(self.__root)
        statsWindow.title("Statistics")

        frame = Frame(statsWindow)

        
        Label(frame, text=self.player1.name).grid(row=0,column=0)


    def __settings(self):
        if self.__gameOnGoing or not self.__loggedIn:
            return

        settingsWindow = Toplevel(self.__root)
        settingsWindow.title("settings")
        frame = Frame(settingsWindow)
        frame.pack()

        Label(frame,text="Timer on")
        def timerChoice():
            if timerOn.get():
                self.__timer = True
            else:
                self.__timer = False
            print(self.__timer)
        timerOn = BooleanVar()
        timerOn.set(False)
        Label(frame, text="hi").grid(row=0, column=0)
        Radiobutton(frame,text="yes",variable=timerOn,command=timerChoice,value=True).grid(row=0)
        Radiobutton(frame,text="no",variable=timerOn,command=timerChoice,value=False).grid(row=1)
        

        

        


    def __playWindow(self, player1, player2, windowName): # AI plays downwards
        self.__gameOnGoing = True
        self.boardLen = 8
        self.player1 = player1
        self.player2 = player2
        self.__game = Game(player1, player2, self.boardLen)
        self.__highlightedSqr = None
        self.__highlightedOriginalCol = None

        gameWindow = Toplevel(self.__root)
        gameWindow.title(windowName)

        player1Frame = Frame(gameWindow)
        Label(player1Frame, text=self.player1.name).grid(row=0,column=0)
        self.numPieces1 = StringVar()
        self.numPieces1.set(self.player1.numPieces)
        Label(player1Frame, textvariable=self.numPieces1).grid(row=0,column=1)
        time1 = StringVar()
        time1.set(self.player1.time)
        Label(player1Frame, textvariable=time1).grid(row=0,column=2)
        player1Frame.grid(row=0,column=0, sticky="NSEW")

        boardFrame = Frame(gameWindow)
        boardFrame.grid(row=1,column=0, sticky="NSEW")
        self.__buttonSymbols = [[None for _ in range(self.boardLen)] for _ in range(self.boardLen)] # making board
        self.__buttonColours = [[None for _ in range(self.boardLen)] for _ in range(self.boardLen)]
        
        for y, x in product(range(self.boardLen), range(self.boardLen)):
            btnCol = ColorVar()
            squareSymbol = StringVar()
            squareSymbol.set(self.__game.at(x,y))
            self.__buttonSymbols[y][x] = squareSymbol
            self.__buttonColours[y][x] = btnCol
            if (x+y)%2== 0:
                btnCol.set(self.__square1col) 
            else:
                btnCol.set(self.__square2col)
            cmd = lambda r=y, c=x: self.__sqrClicked(c,r)
            
            import tkinter.font as font

            #create Font object
            myFont = font.Font(family='Helvetica', size=15)

            Button(
                boardFrame,
                textvariable=squareSymbol,
                command=cmd,
                bg = btnCol,
                height=3,
                width=6,
                font=myFont
                
            ).grid(row=y,column=x)


        player2Frame = Frame(gameWindow)
        Label(player2Frame, text=self.player2.name).grid(row=0,column=0)
        self.numPieces2 = StringVar()
        self.numPieces2.set(self.player2.numPieces)
        Label(player2Frame, textvariable=self.numPieces2).grid(row=0,column=1)
        time2 = StringVar()
        time2.set(self.player2.time)
        Label(player2Frame, textvariable=time2).grid(row=0,column=2)
        player2Frame.grid(row=2,column=0, sticky="S")

        self.__msgText = StringVar()
        self.__msgText.set("")
        Label(gameWindow, textvariable=self.__msgText).grid(row=3,column=0)

        dismissPressed=lambda: self.dismiss(gameWindow)
        
        Button(gameWindow, text="Dismiss", command=dismissPressed).grid(row=4,column=0)
        Button(gameWindow, text="Undo", command=self.__undo).grid(row=4,column=1)

    def __highlight(self, col, row):
        originalColour = self.__buttonColours[row-1][col-1]
        self.__highlightedOriginalCol = originalColour.get()
        self.__highlightedSqr = [row, col]
        self.__buttonColours[row-1][col-1].set("yellow")
      
    def unhighlight(self):
        row, col = self.__highlightedSqr[0]-1, self.__highlightedSqr[1]-1
        self.__buttonColours[row][col].set(self.__highlightedOriginalCol)
        self.__highlightedOriginalCol = None
        self.__highlightedSqr = None

    def dismiss(self, window):
        self.__gameOnGoing = False
        window.destroy()
    

    def __undo(self):
        try:
            self.__game.undo()
            self.__updateBoard()
            self.__handleAI()
        except GameError as e:
            self.__msgText.set(e)
        
    def __sqrClicked(self, x, y):
        if not self.__game.currentPlayer.isAI: # accessing play via button only accessed by humans at their turn
            self.__handleInput(x, y)

    def __handleIfWinner(self):
        self.__winner = self.__game.getWinner()
        if self.__winner:
            self.__msgText.set(f"winner is {self.__winner.name}")
            self.__gameOnGoing = False

    def __handleInput(self, x, y): # 0 indexed
        #self.__buttonColours[4][2].set("yellow")
        if self.__gameOnGoing: #while game ongoing
            x += 1
            y += 1 # 1 indexed
            if self.__highlightedSqr == None: #hasn't picked first square
                try:
                    self.__game.checkIsOwnPiece(x, y)
                    #self.__highlightedSqr = [x, y]
                    self.__msgText.set(f"highlighted {x}, {y}")
                    self.__highlight(x,y)
                except GameError as e:
                    self.__msgText.set(e)
                    
            else: #already picked first square
                if x == self.__highlightedSqr[1] and y == self.__highlightedSqr[0]:
                    self.__msgText.set(f"highlighted square cancelled")
                  #  self.__buttons[self.__highlightedSqr[1]][self.__highlightedSqr[0]].bg ==self.__highlightedSqr[2]
                    #self.__highlightedSqr = None
                    self.unhighlight()

                else:
                    try:
                        self.__game.checkIsVacant(x, y)
                        try:
                            self.__game.play(self.__highlightedSqr[1], self.__highlightedSqr[0], x, y)
                            self.__msgText.set("successful")
                            self.__updateBoard()
                            #self.__highlightedSqr = None
                            self.unhighlight()
                            self.__handleIfWinner()
                        except GameError as e:
                            self.__msgText.set(e)
                            #self.__highlightedSqr = None
                            self.unhighlight()
                    except GameError as e:
                        self.__msgText.set(e)
                        #self.__highlightedSqr = None
                        self.unhighlight()
            self.__handleAI()
                

    def __handleAI(self):
        if self.__game.currentPlayer.isAI:
            output = self.__game.currentPlayer.findMove(self.__game)
            self.__game.play(output[0]+1, output[1]+1, output[2]+1, output[3]+1)
            self.__updateBoard()
            if self.__game.currentPlayer.isAI:
                self.__handleAI()

    def __updateBoard(self):
        for y, x in product(range(self.boardLen), range(self.boardLen)):
            self.__buttonSymbols[y][x].set(self.__game.at(x,y))
        self.numPieces1.set(self.player1.numPieces)
        self.numPieces2.set(self.player2.numPieces)


    def __quit(self):
        self.__root.quit()


    def run(self):
        print("Run")
        self.__root.mainloop()
        pass

class Terminal(Ui):
    def __init__(self, game):
        super().__init__(game)