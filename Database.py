from sqlite3 import *
from Player import *
from contextlib import contextmanager
import pickle


class dbInterface2:
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
    def __init__(self, dbName, playerName):
        self.__dbName = dbName
        self.__playerName = playerName
    
    def loginValid(self, username, password1):
        with self.dbConnnect(self.__dbName) as db:
            statement = f"SELECT * from PlayerInfo WHERE username='{username}' AND password='{password1}'"
            db.execute(statement)
            playerName = db.fetchall()[0]
            if not playerName:
                return False
            self.__playerName = playerName
            return True

    def updatePlayerPreferenceDict(self, dict):
        dict = pickle.dumps(dict)
        with self.dbConnnect(self.__dbName) as db:
            db.execute(f"UPDATE PlayerInfo SET preferenceDict = ? WHERE username = ?", (dict, self.__playerName,))

    def getPlayerPreferenceDict(self):
        with self.dbConnnect(self.__dbName) as db:
            try:
                db.execute(f"SELECT preferenceDict from PlayerInfo WHERE username = '{self.__playerName}'")
                return pickle.loads(db.fetchall()[0][0])
            except:
                return None

    def getPlayerData(self):
        with self.dbConnnect(self.__dbName) as db:
            db.execute("SELECT * from PlayerInfo WHERE username = ?", (self.__playerName,))
            data = db.fetchall()
            return data

    def getPlayerStats(self):
        with self.dbConnnect(self.__dbName) as db:
            print(db.description)
            return list(self.getPlayerData()[0][self.HUMANNUMGAMES:self.AILOSSES+1])

    def getPlayerSavedGame(self, savedGameID):
        with self.dbConnnect(self.__dbName) as db:
            db.execute("SELECT player1, player2, savedGame, gamePreference from PlayerSavedGames WHERE username = ? and savedGameID = ? ", (str(self.__playerName), str(savedGameID),))
            data = db.fetchall()
            player1, player2, game, preference = pickle.loads(data[0][0]), pickle.loads(data[0][1]), pickle.loads(data[0][2]), pickle.loads(data[0][3])
            return player1, player2, game, preference

    def deletePlayerSavedGame(self, savedGameID):
        with self.dbConnnect(self.__dbName) as db:
            db.execute(f"DELETE from PlayerSavedGames WHERE savedGameID = '{savedGameID}'")

    def getAllPlayerSavedGameIDs(self):
        with self.dbConnnect(self.__dbName) as db:
            db.execute(f"SELECT savedGameID from PlayerSavedGames WHERE username = '{self.__playerName}'")
            IDs = db.fetchall()
            return list(map("".join, IDs)) # returns each as a tuple

    def addSavedGame(self, player1, player2, game, savedGameID, currentPreference):
        with self.dbConnnect(self.__dbName) as db:
            pickledPlayer1 = pickle.dumps(player1)
            pickledPlayer2 = pickle.dumps(player2)
            pickledGame = pickle.dumps(game)
            pickledPreference = pickle.dumps(currentPreference)
            
            db.execute("INSERT INTO PlayerSavedGames VALUES (?,?,?,?,?,?)", [savedGameID, pickledPlayer1, pickledPlayer2, pickledGame,  pickledPreference, player1.name])
        
    
    def updateAIstats(self, won): # can be implemented better
        with self.dbConnnect(self.__dbName) as db:
            data = list(self.getPlayerData()[0])
            data[self.AINUMGAMES] += 1
            if won:
                data[self.AIWINS] += 1
            else:
                data[self.AILOSSES] += 1
            db.execute("UPDATE PlayerInfo SET username = ?, AInumGames = ?, AIwins = ?, AIlosses = ?", data)

    def updateHumanStats(self, won):
        with self.dbConnnect(self.__dbName) as db:
            data = list(self.getPlayerData()[0])
            data[self.HUMANNUMGAMES] += 1
            if won:
                data[self.HUMANWINS] += 1
            else:
                data[self.HUMANLOSSES] += 1
            ls = [data[self.HUMANNUMGAMES],data[self.HUMANWINS],data[self.HUMANLOSSES]]
            print("list", ls)
            db.execute("UPDATE PlayerInfo SET humanNumGames = ?, humanWins = ?, humanLosses = ?", ls)


    @contextmanager
    def dbConnnect(self, db):
        conn = connect(db)
        try:
            cur = conn.cursor()
            yield cur
        finally:
            conn.commit()
            conn.close()

