from sqlite3 import *
from Player import *
from contextlib import contextmanager
import pickle


class dbInterface2:
    ...
    NAME = 0
    NUMGAMES = 1
    WINS = 2
    LOSSES = 3
    def __init__(self, dbName, playerName):
        self.__dbName = dbName
        self.__playerName = playerName
    
    def loginValid(self, username, password1):
        with self.dbConnnect(self.__dbName) as db:
            statement = f"SELECT * from Accounts WHERE username='{username}' AND password='{password1}'"
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
            db.execute(f"SELECT preferenceDict from PlayerInfo WHERE username = '{self.__playerName}'")
            return pickle.loads(db.fetchall()[0][0])

    def getPlayerData(self):
        with self.dbConnnect(self.__dbName) as db:
            db.execute("SELECT * from PlayerInfo WHERE name = ?", (self.__playerName,))
            data = db.fetchall()
            return data

    def getPlayerSavedGame(self, savedGameID):
        with self.dbConnnect(self.__dbName) as db:
            db.execute("SELECT savedGame, gamePreference from PlayerSavedGames WHERE username = ? and savedGameID = ? ", (str(self.__playerName), str(savedGameID),))
            data = db.fetchall()
            game, preference = pickle.loads(data[0][0]), pickle.loads(data[0][1])
            return game, preference

    def deletePlayerSavedGame(self, savedGameID):
        with self.dbConnnect(self.__dbName) as db:
            db.execute(f"DELETE from PlayerSavedGames WHERE savedGameID = '{savedGameID}'")

    def getAllPlayerSavedGameIDs(self):
        with self.dbConnnect(self.__dbName) as db:
            db.execute(f"SELECT savedGameID from PlayerSavedGames WHERE username = '{self.__playerName}'")
            IDs = db.fetchall()
            return list(map("".join, IDs)) # returns each as a tuple

    def addSavedGame(self, game, savedGameID, currentPreference):
        with self.dbConnnect(self.__dbName) as db:
            pickledGame = pickle.dumps(game)
            pickledPreference = pickle.dumps(currentPreference)
            db.execute("INSERT INTO PlayerSavedGames VALUES (?,?,?,?)", [savedGameID, self.__playerName, pickledGame, pickledPreference])
        
    
    def update(self, won): # can be implemented better
        with self.dbConnnect(self.__dbName) as db:
            data = list(self.getPlayerData()[0])
            data[self.NUMGAMES] += 1
            if won:
                data[self.WINS] += 1
            else:
                data[self.LOSSES] += 1
            db.execute("UPDATE PlayerInfo SET name = ?, numGames = ?, wins = ?, losses = ?", data)

    @contextmanager
    def dbConnnect(self, db):
        conn = connect(db)
        try:
            cur = conn.cursor()
            yield cur
        finally:
            conn.commit()
            conn.close()


"""
class dbInterface:
    NAME = 0
    NUMGAMES = 1
    WINS = 2
    LOSSES = 3
    def __init__(self, dbName) -> None: # only update player1
        self.__dbName = dbName
        self.__connect()

    def loginValid(self, username, password1):
        statement = f"SELECT * from Accounts WHERE username='{username}' AND password='{password1}'"
        self.__cur.execute(statement)
        playerName = self.__cur.fetchall()
        if not playerName:
            return False
        self.__playerName = playerName
        return True

    def getPlayerData(self):
        self.__cur.execute("SELECT * FROM PlayerInfo WHERE name = ?", (self.__playerName,))
        data = self.__cur.fetchall()
        return data
    
    def getPlayerSavedGame

    def update(self, won): # can be implemented better
        data = list(self.getPlayerData()[0])
        data[self.NUMGAMES] += 1
        if won:
            data[self.WINS] += 1
        else:
            data[self.LOSSES] += 1

        self.__cur.execute("UPDATE PlayerInfo SET name = ?, numGames = ?, wins = ?, losses = ?", data)

    def __connect(self):
        self.__con = connect(self.__dbName)
        self.__cur = self.__con.cursor()
        


class game:
    def __init__(self, player1) -> None:
        self.player1 = player1
    def getWinner(self):
        return self.player1

"""
"""


#a = dbInterface("database.db")
#a.loginValid("MrYun", "123")
"""
