from sqlite3 import *
from Player import *
import pickle

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

cur.execute("DROP TABLE PlayerSavedGames")

cur.execute('''CREATE TABLE PlayerSavedGames
               (savedGameID text PRIMARY KEY, username text, savedGame text)''') 
"""
"""
cur.execute('''CREATE TABLE PlayerInfo (username text PRIMARY KEY, password text, humanNumGames integer, humanWins integer, humanLosses integer, AInumGames integer, AIwins integer, AIlosses integer, preferenceDict text)''')

cur.execute('''CREATE TABLE PlayerSavedGames (savedGameID text PRIMARY KEY, player1 text, player2 text, savedGame text, gamePreference text)''')
"""

#cur.execute("INSERT INTO PlayerInfo VALUES ('MrYun','123', 0, 0, 0, 0, 0, 0,0)")
#cur.execute("ALTER TABLE PlayerSavedGames ADD username text")

#cur.execute("DELETE FROM PlayerSavedGames WHERE username = 'MrYun'")

con.commit()
con.close()
