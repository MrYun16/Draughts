from sqlite3 import *
from Player import *


con = connect("example")
cur = con.cursor()

cur.execute('''CREATE TABLE Accounts
               (username text, password text)''') 
cur.execute("INSERT INTO PlayerInfo VALUES ('Yechan', 0, 0, 0)")
con.commit()
con.close()