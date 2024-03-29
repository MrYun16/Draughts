from sqlite3 import *
from Player import *
from contextlib import contextmanager
import pickle
from Game import GameError

class databaseError(Exception):
    pass

class dbInterface:
    ...
    NAME = 0
    PASSWORD = 1
    HUMANNUMGAMES = 2
    HUMANWINS = 3
    HUMANLOSSES = 4
    AINUMGAMES = 5
    AIWINS = 6
    AILOSSES = 7
    PREFERENCEDICT = 8
    def __init__(self, dbName):
        self.__dbName = dbName

    def createAccount(self, username, password, dict):
        with self.__dbConnect(self.__dbName) as db:
            db.execute(f"SELECT username FROM PlayerInfo")
            createdUsernames = [tupledName[0] for tupledName in db.fetchall()]
            if username in createdUsernames:
                raise databaseError("username already exists")
            db.execute(f"INSERT INTO PlayerInfo VALUES (?,?,?,?,?,?,?,?,?)", (username,password,0,0,0,0,0,0,pickle.dumps(dict)))






    def loginValid(self, username, password1):
        with self.__dbConnect(self.__dbName) as db:
            statement = f"SELECT * from PlayerInfo WHERE username='{username}' AND password='{password1}'"
            db.execute(statement)
            try:
                if len(db.fetchall()) == 0:
                    raise databaseError("enter again")
                self.__playerName = username
                return True
            except:
                return False



    def updatePlayerPreferenceDict(self, dict):
        ############################################
        # CATEGORY B MODEL: TEXT FILES
        # Dictionary converted to a binary text file
        ############################################
        dict = pickle.dumps(dict)
        with self.__dbConnect(self.__dbName) as db:
            db.execute(f"UPDATE PlayerInfo SET preferenceDict = ? WHERE username = ?", (dict, self.__playerName,))

    def getPlayerPreferenceDict(self):
        with self.__dbConnect(self.__dbName) as db:
            
            db.execute(f"SELECT preferenceDict from PlayerInfo WHERE username = '{self.__playerName}'")
            ############################################
            # CATEGORY B MODEL: TEXT FILES
            # text file converted back to dictionary and
            # returned
            ############################################
            return pickle.loads(db.fetchall()[0][0])

    def getPlayerData(self):
        with self.__dbConnect(self.__dbName) as db:
            db.execute("SELECT * from PlayerInfo WHERE username = ?", (self.__playerName,))
            data = db.fetchall()
            return data

    def getPlayerStats(self):
        with self.__dbConnect(self.__dbName) as db:
           
            return list(self.getPlayerData()[0][self.HUMANNUMGAMES:self.AILOSSES+1])

    def getPlayerSavedGame(self, savedGameID):
        with self.__dbConnect(self.__dbName) as db:
            db.execute("SELECT player1, player2, savedGame, gamePreference from PlayerSavedGames WHERE username = ? and savedGameID = ? ", (str(self.__playerName), str(savedGameID),))
            data = db.fetchall()
            ############################################
            # CATEGORY B MODEL: TEXT FILES
            # text files converted back to dictionary and
            # class instances
            ############################################
            player1, player2, game, preference = pickle.loads(data[0][0]), pickle.loads(data[0][1]), pickle.loads(data[0][2]), pickle.loads(data[0][3])
            return player1, player2, game, preference

    def deletePlayerSavedGame(self, savedGameID):
        with self.__dbConnect(self.__dbName) as db:
            db.execute(f"DELETE from PlayerSavedGames WHERE savedGameID = '{savedGameID}'")

    def getAllPlayerSavedGameIDs(self):
        with self.__dbConnect(self.__dbName) as db:
            
            db.execute(f"SELECT savedGameID from PlayerSavedGames WHERE username = '{self.__playerName}' ")
            IDs = db.fetchall()
            return list(map("".join, IDs)) # returns each as a tuple

    def addSavedGame(self, player1, player2, game, savedGameID, currentPreference):
        with self.__dbConnect(self.__dbName) as db:
            ############################################
            # CATEGORY B MODEL: TEXT FILES
            # converting classes and dictionary to 
            # text file
            ############################################
            pickledPlayer1 = pickle.dumps(player1)
            pickledPlayer2 = pickle.dumps(player2)
            pickledGame = pickle.dumps(game)
            pickledPreference = pickle.dumps(currentPreference)
            
            db.execute("INSERT INTO PlayerSavedGames VALUES (?,?,?,?,?,?)", [savedGameID, pickledPlayer1, pickledPlayer2, pickledGame,  pickledPreference, player1.name])
        
    
    def updateAIstats(self, won): 
        with self.__dbConnect(self.__dbName) as db:
            data = list(self.getPlayerData()[0])
            data[self.AINUMGAMES] += 1
            if won:
                data[self.AIWINS] += 1
            else:
                data[self.AILOSSES] += 1
            ls = [data[self.AINUMGAMES],data[self.AIWINS],data[self.AILOSSES]]
            db.execute("UPDATE PlayerInfo SET AInumGames = ?, AIwins = ?, AIlosses = ?", ls)

    def updateHumanStats(self, won):
        with self.__dbConnect(self.__dbName) as db:
            data = list(self.getPlayerData()[0])
            data[self.HUMANNUMGAMES] += 1
            if won:
                data[self.HUMANWINS] += 1
            else:
                data[self.HUMANLOSSES] += 1
            ls = [data[self.HUMANNUMGAMES],data[self.HUMANWINS],data[self.HUMANLOSSES]]
     
            db.execute("UPDATE PlayerInfo SET humanNumGames = ?, humanWins = ?, humanLosses = ?", ls)


    @contextmanager
    def __dbConnect(self, db):
        conn = connect(db)
        try:
            cur = conn.cursor()
            yield cur
        finally:
            conn.commit()
            conn.close()

