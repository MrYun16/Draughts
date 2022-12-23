from msilib.schema import Font
from turtle import width
from Game import GameError, Game, TimeError
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
    TIME = "time"
    BOARDLEN = "boardLen"
    BOARDCOLOUR = "boardColour"


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
        self.__username = "MrYun" # string
        self.__loggedIn = True # needs to be False
        self.__overallPreference = {self.BOARDLEN:8, self.BOARDCOLOUR:"brown", self.TIME:3600}

        #Label(frame, textvariable=f"welcome {self.__username}").pack()
        menuHeader = StringVar()
        menuHeader.set(f"welcome {self.__username}")
        Label(frame, textvariable=menuHeader).pack()
        #self.__username.set("MrYun") # only for testing
        
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
            self.__username = self.__username.get()
            self.__loggedIn = True
        else:
            return
        

    def __AImenu(self):
        if self.__gameOnGoing:
            return

        newOverallPreference = self.__overallPreference.copy()
        newOverallPreference[self.TIME] = -1 # no time allowed for AI
        AIwindow = Toplevel(self.__root)
        AIwindow.title("AI difficulty")
        boardLen = self.__overallPreference[self.BOARDLEN]
        player1 = Player(self.__username, "white", 1, boardLen)
        clickedEasy=lambda player2=randomAI("EASY AI","black",-1,boardLen):self.__playWindow(player1, player2, Game(player1,player2,boardLen), "Easy", newOverallPreference)
        clickedHard=lambda player2=hardAI("HARD AI","black",-1,boardLen):self.__playWindow(player1, player2, Game(player1,player2,boardLen), "Hard", newOverallPreference)
        lvlsFrame = Frame(AIwindow)
        Button(lvlsFrame, text="Easy", command = clickedEasy, pady=20).grid(row=0,column=0)
        Button(lvlsFrame, text="Hard", command = clickedHard, pady=20).grid(row=1,column=0)
        lvlsFrame.pack()

        #player1, player2, game, windowName, preference
    
    def __onePlayer(self):
        if self.__gameOnGoing or not self.__loggedIn:
            return
        self.__AImenu()

    def __twoPlayer(self):

        if self.__gameOnGoing or not self.__loggedIn:
            return
        boardLen = self.__overallPreference[self.BOARDLEN]
        player1 = Player(self.__username, "white", 1, boardLen)
        player2 = Player("Player2", "black", -1, boardLen)

        game = Game(player1, player2, boardLen)
        self.__playWindow(player1, player2, game, "Two Player", self.__overallPreference)
        self.__gameOnGoing = True

    def __statistics(self):
        if self.__gameOnGoing or not self.__loggedIn:
            return
        statsWindow = Toplevel(self.__root)
        statsWindow.title("Statistics")
        statsWindow.geometry("200x300")

        frame = Frame(statsWindow)
        frame.pack()
        Label(frame, text=self.__username).grid(row=0,column=0)
        stats = self.__dbInterface.getPlayerStats()
        
        Label(frame, text="Two Player").grid(row=0,column=0)
        Label(frame, text="games").grid(row=1,column=0)
        Label(frame, text=stats[0]).grid(row=1,column=1)
        Label(frame, text="wins").grid(row=2,column=0)
        Label(frame, text=stats[1]).grid(row=2,column=1)
        Label(frame, text="loss").grid(row=3,column=0)
        Label(frame, text=stats[2]).grid(row=3,column=1)
        Label(frame, text="AI").grid(row=4,column=0)
        Label(frame, text="games").grid(row=5,column=0)
        Label(frame, text=stats[3]).grid(row=5,column=1)
        Label(frame, text="wins").grid(row=6,column=0)
        Label(frame, text=stats[4]).grid(row=6,column=1)
        Label(frame, text="loss").grid(row=7,column=0)
        Label(frame, text=stats[5]).grid(row=7,column=1)


    def __settings(self):

        if self.__gameOnGoing or not self.__loggedIn:
            return
        self.__overallPreference = self.__dbInterface.getPlayerPreferenceDict()
        if self.__overallPreference is None:
            self.__overallPreference = {self.BOARDLEN:8, self.BOARDCOLOUR:"brown", self.TIME:3600}

        def updatePreference(key, value):
            self.__overallPreference[key] = value
            self.__dbInterface.updatePlayerPreferenceDict(self.__overallPreference)
        
        settingsWindow = Toplevel(self.__root)
        settingsWindow.geometry("400x400")
        settingsWindow.title("settings")
        frame = Frame(settingsWindow)
        frame.pack()

        initialTime = IntVar()
        initialTime.set(self.__overallPreference[self.TIME])
        Label(frame, text="Select Time:").grid(row=3,column=1)
        timeInWordsToDemi = {
            "1min":3600,
            "3mins":10800,
            "5mins":18000,
            "10mins":36000,
            "30mins":108000,
            "1hr":216000,
            "1hr30mins":324000,
            "none":-1
        }
        timeInWords = StringVar()
        for word, demi in timeInWordsToDemi.items():
            if demi == self.__overallPreference[self.TIME]:
                timeInWords.set(word)
                print("done")
                break

        timerMenu = OptionMenu(frame, timeInWords, "1min", "3mins", "5mins", "10mins", "30mins", "1hr", "1hr30mins", "none", command= lambda e: updatePreference(self.TIME, timeInWordsToDemi[timeInWords.get()]))
        timerMenu.config(width=20)
        timerMenu.grid(row=3,column=2)

        boardLen = IntVar()
        boardLen.set(self.__overallPreference[self.BOARDLEN])
        Label(frame, text="Select board length:").grid(row=4,column=1)
        boardLenMenu = OptionMenu(frame, boardLen, 6, 8, command=lambda e: updatePreference(self.BOARDLEN, boardLen.get()))
        boardLenMenu.config(width=20)
        boardLenMenu.grid(row=4,column=2,sticky="EW")

        boardColour = StringVar()
        boardColour.set(self.__overallPreference[self.BOARDCOLOUR])
        Label(frame, text="Select board colour:").grid(row=5,column=1)
        boardMenu = OptionMenu(frame, boardColour, "blue", "brown", "green", "red", command=lambda e: updatePreference(self.BOARDCOLOUR, boardColour.get()))
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
        player1, player2, game, preference = self.__dbInterface.getPlayerSavedGame(gameID)
        loadWin.destroy()
        self.__dbInterface.deletePlayerSavedGame(gameID)

        clockDisplayString1 = StringVar()
        clockDisplayString2 = StringVar()

        player1.createClock(player1.timeBeforeSaved, clockDisplayString1, self.__root)
        player2.createClock(player2.timeBeforeSaved, clockDisplayString2, self.__root)

        game.updatePlayer1(player1)
        game.updatePlayer2(player2)

        self.__playWindow(player1, player2, game, "Loaded Game", preference)

        
    def __playWindow(self, player1, player2, game, windowName, preference): # AI plays downwards
        self.__gameOnGoing = True
        self.__player1 = player1
        self.__player2 = player2
        boardLen = preference[self.BOARDLEN]
        self.__game = game # making game
        self.__highlightedSqr = None
        self.__highlightedOriginalCol = None    

        gameWindow = Toplevel(self.__root)
        gameWindow.title(windowName)

        player1Frame = Frame(gameWindow)
        self.numPieces1 = StringVar()
        self.numPieces1.set(self.__player1.numPieces)

        clockDisplayString1 = StringVar()
        clockDisplayString2 = StringVar()

        player1.createClock(preference[self.TIME], clockDisplayString1, self.__root)
        player2.createClock(preference[self.TIME], clockDisplayString2, self.__root)

        self.__player1.clock.timeLeft.trace("w", self.__handleIfWinner)
        self.__player2.clock.timeLeft.trace("w", self.__handleIfWinner)
        Label(player1Frame, textvariable=self.__player1.clock.clockDisplayString, font=("Times",24)).grid(row=0, column=2)
        

        Label(player1Frame, text=self.__player1.name, font=("Times",24)).grid(row=0, column=0)
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
                sqrCol.set(preference[self.BOARDCOLOUR])
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
        self.numPieces2.set(self.__player2.numPieces)
        Label(player2Frame, text=self.__player2.name, font=("Times",24)).grid(row=0,column=0)
        Label(player2Frame, textvariable=self.numPieces2, font=("Times",24)).grid(row=0,column=1)
        player2Frame.grid(row=2,column=0, sticky="W")

        Label(player2Frame, textvariable=self.__player2.clock.clockDisplayString, font=("Times",24)).grid(row=0, column=2, sticky="E")
        
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
        if self.__gameOnGoing:
            self.__player1.deleteClock() # clock contains tkinter, tkinter cannot be pickled
            self.__player2.deleteClock()

            ID = datetime.datetime.now().strftime("%H:%M:%S")

            self.__dbInterface.addSavedGame(self.__player1, self.__player2, self.__game, ID, self.__overallPreference)
            self.__gameOnGoing = False
            gameWin.destroy()
        

    def updateScoreLabel(self):
        self.numPieces2.set(self.__player2.numPieces)
        self.numPieces1.set(self.__player1.numPieces)
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

    def __handleIfWinner(self, *args):
        self.__winner = self.__game.getWinner()
        if self.__winner:
            self.__msgText.set(f"winner is {self.__winner.name}")
            self.__gameOnGoing = False
            self.__player1.clock.stop()
            self.__player2.clock.stop()
        try:
            if self.__player1.clock.timeLeft.get() and not self.__player2.clock.timeLeft.get():
                self.__msgText.set(f"winner is {self.__player1.name}")
                self.__gameOnGoing = False
            elif self.__player2.clock.timeLeft.get() and not self.__player1.clock.timeLeft.get():
                self.__msgText.set(f"winner is {self.__player2.name}")
                self.__gameOnGoing = False
        except:
            pass

        if not self.__gameOnGoing: # i.e. is winner
            if self.__player2.isAI:
                if self.__winner == self.__player1:
                    self.__dbInterface.updateAIstats(True)
                else:
                    self.__dbInterface.updateAIstats(False)
            else:
                if self.__winner == self.__player1:
                    self.__dbInterface.updateHumanStats(True)
                else:
                    self.__dbInterface.updateHumanStats(False)

    def __handleInput(self, x, y, preference): # inputs 0 indexed
        if self.__gameOnGoing: #while game ongoing
            
           # if self.__game.boardHistoryLen() == 1:
            #    self.__player1Clock.start()
            x += 1
            y += 1
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
                            #self.switchTimers()
                        except GameError as e:
                            self.__msgText.set(e)
                            self.unhighlight()
                        except TimeError as e:
                            self.__msgText.set(e)
                    except GameError as e:
                        self.__msgText.set(e)
                        self.unhighlight()
            self.__handleAI(preference)

    def switchTimers(self): # this is called after play occurs
        self.__game.currentPlayer().clock.start()
        self.__game.nonCurrentPlayer().clock.stop()

    def __handleAI(self, preference):
        if self.__game.currentPlayer.isAI:
            output = self.__game.currentPlayer.findMove(self.__game)
            self.__game.play(output[0], output[1], output[2], output[3])
            self.__updateBoard(preference)
            if self.__game.currentPlayer.isAI:
                self.__handleAI(preference)

    def __updateBoard(self, preference):
        boardLen = preference[self.BOARDLEN]
        for y, x in product(range(boardLen), range(boardLen)):
            self.__buttonSymbols[y][x].set(self.__game.at(x,y))
        self.numPieces1.set(self.__player1.numPieces)
        self.numPieces2.set(self.__player2.numPieces)


    def __quit(self):
        self.__root.quit()


    def run(self):
        self.__root.mainloop()
        pass

class Terminal(Ui):
    def __init__(self, game):
        super().__init__(game)