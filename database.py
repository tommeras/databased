import sqlite3
con = sqlite3.connect("kaffe.db")
cursor = con.cursor()
#cursor.execute("SELECT * FROM sqlite_master")

#Lager tabellen Gård
cursor.execute("""CREATE TABLE IF NOT EXISTS Gård (GårdId INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT, 
Høyde NUMERIC NOT NULL, 
Region TEXT NOT NULL, 
FOREIGN KEY (Region) REFERENCES Region (Region)) """)

#Lager tabellen Region
cursor.execute("""CREATE TABLE IF NOT EXISTS Region (Region TEXT NOT NULL UNIQUE PRIMARY KEY, Land TEXT NOT NULL)""")


#Lager tabellen Brenneri
cursor.execute("""CREATE TABLE IF NOT EXISTS Brenneri (BrenneriId INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
 Navn TEXT NOT NULL)""")

#Lager tabellen Bønne
cursor.execute("""CREATE TABLE IF NOT EXISTS Bønne (BønneId INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
 Art TEXT NOT NULL)""")

#Lager tabellen Bruker
cursor.execute("""CREATE TABLE IF NOT EXISTS Bruker (Epost TEXT NOT NULL UNIQUE PRIMARY KEY,
 Passord TEXT NOT NULL, FulltNavn TEXT)""")

#Lager tabellen Behandlingsmetode
cursor.execute("""CREATE TABLE IF NOT EXISTS Behandlingsmetode (BehandlingsId INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
 Beskrivelse TEXT NOT NULL, Navn TEXT NOT NULL)""")

#Lager tabellen Typer
cursor.execute("""CREATE TABLE IF NOT EXISTS Typer (
    KaffepartiId INTEGER NOT NULL,
    BønneId INTEGER NOT NULL,
    PRIMARY KEY(BønneId, KaffepartiId))""")

#Lager tabellen Dyrkes Av
cursor.execute("""CREATE TABLE IF NOT EXISTS DyrkesAv (
    GårdId INTEGER NOT NULL,
    BønneId INTEGER NOT NULL,
    PRIMARY KEY(BønneId, GårdId))""")

#Lager tabellen Kaffe
cursor.execute("""CREATE TABLE IF NOT EXISTS Kaffe (
    KaffeId INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    Navn TEXT NOT NULL,
    Brenningsgrad TEXT NOT NULL, 
    Produksjonsdato TEXT NOT NULL,
    Beskrivelse TEXT,
    Kilospris NUMERIC NOT NULL, 
    BrenneriId INTEGER NOT NULL, 
    KaffepartiId INTEGER NOT NULL)""")


#Lager tabellen Kaffesmaking
cursor.execute("""CREATE TABLE IF NOT EXISTS Kaffesmaking (
    KaffesmakingId INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    Smaksnotat TEXT NOT NULL,
    Poeng INTEGER,
    Dato TEXT NOT NULL,
    BrukerId TEXT NOT NULL, 
    KaffeId INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (BrukerId) REFERENCES Bruker (BrukerId),
    FOREIGN KEY (KaffeId) REFERENCES Kaffe (KaffeId))""")


con.commit()


con.close()

