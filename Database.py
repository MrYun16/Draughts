from sqlite3 import *
from Player import *



class dbInterface:
    NAME = 0
    NUMGAMES = 1
    WINS = 2
    LOSSES = 3
    def __init__(self, dbName, player1, game) -> None: # only update player1
        self.__dbName = dbName
        self.__player1 = player1
        self.__game = game
        self.__connect()

    def getData(self):
        self.__cur.execute("SELECT * FROM PlayerInfo WHERE name = ?", (self.__player1.name,))
        data = self.__cur.fetchall()
        return data
    
    def update(self): # can be implemented better
        data = list(self.getData()[0])
        data[self.NUMGAMES] += 1
        if self.__player1 == self.__game.getWinner():
            data[self.WINS] += 1
        else:
            data[self.LOSSES] += 1

        self.__cur.execute("UPDATE PlayerInfo SET name = ?, numGames = ?, wins = ?, losses = ?", data)

    def __connect(self):
        self.__con = connect(self.__dbName)
        self.__cur = self.__con.cursor()
        
        #self.__cur.execute('''CREATE TABLE PlayerInfo
        #               (name text, numGames real, wins real, losses real)''') 
        #self.__cur.execute("INSERT INTO PlayerInfo VALUES ('Yechan', 0, 0, 0)")
        #self.__con.commit()
        #self.__con.close()

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