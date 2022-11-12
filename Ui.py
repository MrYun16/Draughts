from msilib.schema import Font
from turtle import width
from Game import GameError, Game
from tkinter import *
from Player import Player, randomAI, hardAI
from itertools import product
from Database import dbInterface2
from clock import Clock
import time
import tkinter.font as font
import pickle
import datetime
from tkmacosx import ColorVar



class Ui:
    def __init__(self):
        self.__game = Game(Player("Player1", None, 1), Player("Player2", None, -1), 8)

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
        root.title("Draughts")
        root.geometry("200x400")
        frame = Frame(root)
        frame.pack()
        self.__root = root
        self.__gameOnGoing = False
        self.__dbInterface = dbInterface2("database.db", "MrYun")
        self.__login()
        self.__name = "MrYun" # string
        self.__loggedIn = True # needs to be False
        self.__overallPreference = {"boardLen":8, "boardColour":"brown", "time":120}

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
            text="Load Games",
            command=self.__loadGame
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
            return
        

    def __AImenu(self):
        if self.__gameOnGoing:
            return
        AIwindow = Toplevel(self.__root)
        AIwindow.title("AI difficulty")
        boardLen = self.__overallPreference["boardLen"]
        # NEEDS TO BE FIXED
        player1 = Player(self.__name, "white", 1, boardLen)
        clickedEasy=lambda player2=randomAI("Player2","black",-1,boardLen):self.__playWindow(player1, player2, Game(player1,player2,boardLen), "Easy")
        clickedHard=lambda player2=hardAI("Player2","black",-1,boardLen):self.__playWindow(player1, player2, Game(player1,player2,boardLen), "Hard")
        lvlsFrame = Frame(AIwindow)
        Button(lvlsFrame, text="Easy", command = clickedEasy, pady=20).grid(row=0,column=0)
        Button(lvlsFrame, text="Hard", command = clickedHard, pady=20).grid(row=1,column=0)
        lvlsFrame.pack()
    
    def __onePlayer(self):
        if self.__gameOnGoing or not self.__loggedIn:
            return
        self.__AImenu()

    def __twoPlayer(self):

        if self.__gameOnGoing or not self.__loggedIn:
            return
        boardLen = self.__overallPreference["boardLen"]
        player1 = Player(self.__name, "white", 1, boardLen)
        player2 = Player("Player2", "black", -1, boardLen)
        game = Game(player1, player2, boardLen)
        self.__playWindow(player1, player2, game, "Two Player", self.__overallPreference)
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
        self.__overallPreference = self.__dbInterface.getPlayerPreferenceDict()
        def updatePreference(key, value):
            self.__overallPreference[key] = value
            self.__dbInterface.updatePlayerPreferenceDict(self.__overallPreference)
        
        settingsWindow = Toplevel(self.__root)
        settingsWindow.geometry("400x400")
        settingsWindow.title("settings")
        frame = Frame(settingsWindow)
        frame.pack()

        initialTime = IntVar()
        initialTime.set(self.__overallPreference["time"])
        Label(frame, text="Select Time:").grid(row=3,column=1)
        timerMenu = OptionMenu(frame, initialTime, 60, 120, 600, 1200, -1, command= lambda e: updatePreference("time", initialTime.get()))
        timerMenu.config(width=20)
        timerMenu.grid(row=3,column=2)

        boardLen = IntVar()
        boardLen.set(self.__overallPreference["boardLen"])
        Label(frame, text="Select board length:").grid(row=4,column=1)
        boardLenMenu = OptionMenu(frame, boardLen, 6, 8, command=lambda e: updatePreference("boardLen", boardLen.get()))
        boardLenMenu.config(width=20)
        boardLenMenu.grid(row=4,column=2,sticky="EW")

        boardColour = StringVar()
        boardColour.set(self.__overallPreference["boardColour"])
        Label(frame, text="Select board colour:").grid(row=5,column=1)
        boardMenu = OptionMenu(frame, boardColour, "blue", "brown", "green", "red", command=lambda e: updatePreference("boardColour", boardColour.get()))
        boardMenu.config(width=20)
        boardMenu.grid(row=5,column=2,sticky="EW")

    

    def __loadGame(self):
        loadGameWindow = Toplevel(self.__root)
        loadGameWindow.geometry("400x400")
        loadGameWindow.title("Saved Games")
        IDs = self.__dbInterface.getAllPlayerSavedGameIDs()
        nameToID = {}
        for i, ID in enumerate(IDs):
            nameToID[i+1] = ID
        
        myFont = font.Font(family='Helvetica', size=15)
        savedGamesFrame = Frame(loadGameWindow)
        Label(loadGameWindow, text="Saved Games", font=myFont, anchor=CENTER).grid(row=1, column=1)
        
        for name in range(1, len(IDs)+1):
            cmd = lambda ID=nameToID[name]: self.loadGame(ID, loadGameWindow)
            Button(
                savedGamesFrame,
                text=name,
                command=cmd,
                height=3,
                width=6,
                font=myFont
            ).grid(row=name//3,column=name%3)
        savedGamesFrame.grid(row=2, column=1, sticky="S")

   
    def loadGame(self, gameID, loadWin):
        game, preference = self.__dbInterface.getPlayerSavedGame(gameID)
        player1 = Player(self.__name, "white", 1, 8)
        player2 = Player("Player2", "black", -1, 8)
        loadWin.destroy()
        self.__dbInterface.deletePlayerSavedGame(gameID)
        self.__playWindow(player1, player2, game, "Loaded Game", preference)

        

    def __playWindow(self, player1, player2, game, windowName, preference): # AI plays downwards
        self.__gameOnGoing = True
        self.player1 = player1
        self.player2 = player2
        boardLen = preference["boardLen"]
        self.__game = game # making game
        self.__highlightedSqr = None
        self.__highlightedOriginalCol = None    

        gameWindow = Toplevel(self.__root)
        gameWindow.title(windowName)

        player1Frame = Frame(gameWindow)
        self.numPieces1 = StringVar()
        self.numPieces1.set(self.player1.numPieces)
        
        self.clockDisplay1 = StringVar()
        self.player1Clock = Label(player1Frame, textvariable=self.clockDisplay1, font=("Times",24))
        self.player1Clock.grid(row=0, column=2)
        playerClock = Clock(300, self.clockDisplay1, self.__root)
        try:
            playerClock.start()
        except:
            print("it ended")

        Label(player1Frame, text=self.player1.name, font=("Times",24)).grid(row=0, column=0)
        Label(player1Frame, textvariable=self.numPieces1, font=("Times",24)).grid(row=0, column=1)
        player1Frame.grid(row=0,column=0, sticky="W")

        boardFrame = Frame(gameWindow)
        boardFrame.grid(row=1,column=0, sticky="NSEW")
        self.__buttonSymbols = [[None for _ in range(boardLen)] for _ in range(boardLen)] # making board
        self.__buttonColours = [[None for _ in range(boardLen)] for _ in range(boardLen)]
        
        for y, x in product(range(boardLen), range(boardLen)):
            sqrCol = StringVar()
            squareSymbol = StringVar()
            squareSymbol.set(self.__game.at(x,y))
            self.__buttonSymbols[y][x] = squareSymbol
            self.__buttonColours[y][x] = sqrCol
            if (x+y)%2== 0:
                sqrCol.set("white")
            else:
                sqrCol.set(preference["boardColour"])
            cmd = lambda r=y, c=x: self.__sqrClicked(c,r,preference)
            #create Font object
            myFont = font.Font(family='Helvetica', size=15)
            Button(
                boardFrame,
                textvariable=squareSymbol,
                command=cmd,
                bg = sqrCol,
                height=3,
                width=6,
                font=myFont
            ).grid(row=y,column=x)
        
        player2Frame = Frame(gameWindow)
        self.numPieces2 = StringVar()
        self.numPieces2.set(self.player2.numPieces)
        Label(player2Frame, text=self.player2.name, font=("Times",24)).grid(row=0,column=0)
        Label(player2Frame, textvariable=self.numPieces2, font=("Times",24)).grid(row=0,column=1)
        timeString2 = StringVar()
 
        Label(player2Frame, text=timeString2.get(), font=("Times",24)).grid(row=0,column=1, sticky="E")
        player2Frame.grid(row=2,column=0, sticky="W")

        self.__msgText = StringVar()
        self.__msgText.set("")
        Label(gameWindow, textvariable=self.__msgText).grid(row=3,column=0)

        dismissPressed=lambda: self.dismiss(gameWindow)
        continuePressed=lambda : self.__saveGame(gameWindow)
        undoPressed=lambda : self.__undo(preference)

        Button(gameWindow, text="Dismiss", command=dismissPressed).grid(row=4,column=2)
        Button(gameWindow, text="Undo", command=undoPressed).grid(row=4,column=3)
        Button(gameWindow, text="Continue for later", command=continuePressed).grid(row=4,column=1)

    def __saveGame(self, gameWin): # ADD GAME TO ARGUMENT later
        ID = datetime.datetime.now().strftime("%H:%M:%S")
        self.__dbInterface.addSavedGame(self.__game, ID, self.__overallPreference)
        self.__gameOnGoing = False
        gameWin.destroy()

        

    def updateScoreLabel(self):
        self.numPieces2.set(self.player2.numPieces)
        self.numPieces1.set(self.player1.numPieces)
        print(self.numPieces2.get(), self.numPieces1.get())

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

    def __undo(self, preference):
        try:
            self.__game.undo()
            self.__updateBoard(preference)
            self.__handleAI(preference)
        except GameError as e:
            self.__msgText.set(e)
        
    def __sqrClicked(self, x, y, preference):
        if not self.__game.currentPlayer.isAI: # accessing play via button only accessed by humans at their turn
            self.__handleInput(x, y, preference)

    def __handleIfWinner(self):
        self.__winner = self.__game.getWinner()
        if self.__winner:
            self.__msgText.set(f"winner is {self.__winner.name}")
            self.__gameOnGoing = False

    def __handleInput(self, x, y, preference): # 0 indexed
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
                            self.__updateBoard(preference)
                            self.unhighlight()
                            self.__handleIfWinner()
                          #  self.updateScoreLabel()
                        except GameError as e:
                            self.__msgText.set(e)
                            self.unhighlight()
                    except GameError as e:
                        self.__msgText.set(e)
                       
                        self.unhighlight()
            self.__handleAI(preference)

    def __handleAI(self, preference):
        if self.__game.currentPlayer.isAI:
           
            output = self.__game.currentPlayer.findMove(self.__game)
            self.__game.play(output[0], output[1], output[2], output[3])
            self.__updateBoard(preference)
            #self.updateScoreLabel()
            if self.__game.currentPlayer.isAI:
                self.__handleAI(preference)

    def __updateBoard(self, preference):
        boardLen = preference["boardLen"]
        for y, x in product(range(boardLen), range(boardLen)):
            self.__buttonSymbols[y][x].set(self.__game.at(x,y))
        self.numPieces1.set(self.player1.numPieces)
        self.numPieces2.set(self.player2.numPieces)


    def __quit(self):
        self.__root.quit()


    def run(self):
        self.__root.mainloop()
        pass

class Terminal(Ui):
    def __init__(self, game):
        super().__init__(game)