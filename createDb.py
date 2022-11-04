from sqlite3 import *
from Player import *


con = connect("database.db")
cur = con.cursor()

"""cur.execute('''CREATE TABLE Accounts
               (username text PRIMARY KEY, password text)''') 
cur.execute('''CREATE TABLE PlayerInfo
               (username text PRIMARY KEY, numGames real, wins real, losses real)''') 
cur.execute("INSERT INTO PlayerInfo VALUES ('MrYun', 0, 0, 0)")
cur.execute("INSERT INTO Accounts VALUES ('MrYun', '123')")
con.commit()
con.close()
"""
cur.execute("DROP TABLE PlayerSavedGames")

cur.execute('''CREATE TABLE PlayerSavedGames
               (savedGameID text PRIMARY KEY, username text, savedGame text)''') 



cur.execute("INSERT INTO PlayerSavedGames VALUES ('04/11', 'MrYun', '')")

con.commit()
con.close()
