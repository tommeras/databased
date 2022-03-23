import sqlite3
con = sqlite3.connect("kaffe.db")
cursor = con.cursor()
#cursor.execute("SELECT * FROM sqlite_master")
cursor.execute('''SELECT *''')
con.commit()


con.close()

