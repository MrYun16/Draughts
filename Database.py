from sqlite3 import *
from Player import *



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
g = game(Player("Yechan", "white", 1))
a = dbInterface("example", Player("Yechan", "white", 1), g)
print(a.getData())
a.update()
print(a.getData())
a.update()
print(a.getData())
"""
#a = dbInterface("database.db")
#a.loginValid("MrYun", "123")