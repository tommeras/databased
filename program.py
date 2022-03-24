from datetime import date
import sqlite3

#Her lager vi connection
con = sqlite3.connect("kaffe.db")
cursor = con.cursor()

def FørsteBrukerHistorie():
    # epost = input("Hva er E-posten din? ")
    # passord = input("Hva er passordet ditt? ")
    # cursor.execute("""SELECT * FROM Bruker""")
    # result = cursor.fetchall()
    # b = False
    # for x in result:
    #     if(epost == x[0] and passord == x[1]):
    #         b=True
    # if(b):
    #     print("Du er logget inn")
    # else:
    #     print("Feil brukernavn eller passord\nDu må skrive det inn på nytt")
    #     FørsteBrukerHistorie()
    dato = date.today()
    år = date.year
    måned = date.month
    dag = date.day



    brenneri = input("Hvilket brenneri er kaffen fra? ")
    kaffe = input("Hva er Kaffens navn? ")
    poeng = input("Hvor mange poeng av 10 vil du gi den? ")
    notat = input("Skriv ned noen tanker om kaffen: ")

    cursor.execute(f"""SELECT KaffeId from Kaffe WHERE Kaffe.Navn like '{kaffe}'""")
    result = cursor.fetchone()
    kaffeId = result[0]

    cursor.execute(f'''INSERT INTO Kaffesmaking (Smaksnotat, Poeng, BrukerId, År, Måned, Dag , KaffeId)
            VALUES ("{notat}", {poeng}, "test@test.test", 2022, 03, 24,{kaffeId})''')
            #jobba litt, men ble trøtt. Det som mangler her er å få til å 
            #gjøre om datetime objekter til integers sånn at vi kan bruke dem
    con.commit()

def AndreBrukerHistorie():
    cursor.execute("""SELECT FulltNavn, count(BrukerId) as Antall 
                        FROM Kaffesmaking
                        INNER JOIN Bruker 
                        on Kaffesmaking.BrukerId = Bruker.Epost
                        WHERE År = 2022
                        GROUP by Bruker.FulltNavn
                        ORDER by Antall DESC""")
    result = cursor.fetchall()
    print(" ")
    print("Resultater:")
    tabell = []
    for x in result:
        insert = [x[0], x[1]]
        tabell.append(insert)
    for rad in tabell:
        print("{: >20} {: >10}".format(*rad))

def TredjeBrukerHistorie():
    cursor.execute(""" SELECT Brenneri.Navn as BrenneriNavn, Kaffe.Navn as KaffeNavn , Kaffe.Kilospris as Pris,
                        round(avg(Kaffesmaking.Poeng),3) as GjennomsnittsScore From Kaffe 
                        INNER JOIN Brenneri on Kaffe.BrenneriId = Brenneri.BrenneriId
                        JOIN Kaffesmaking on Kaffesmaking.KaffeId = Kaffe.KaffeId
                        GROUP BY KaffeNavn
                        ORDER BY (Kaffe.Kilospris/avg(Kaffesmaking.Poeng))""")

    result = cursor.fetchall()
    print(" ")
    print("Resultater: ")
    tabell = []
    for x in result:
        insert = [x[0], x[1], x[2], x[3]]
        tabell.append(insert)
    for rad in tabell:
        print("{: >25} {: >20} {: >5} {: >10}".format(*rad))


def FjerdeBrukerHistorie():
    beskrivelse = input("Hvilet ord skal kaffen være beskrevet med? ")
    cursor.execute(f"""SELECT Brenneri.Navn as BrenneriNavn, Kaffe.Navn as KaffeNavn FROM Kaffe 
                    INNER JOIN Brenneri on Kaffe.BrenneriId = Brenneri.BrenneriId
                    WHERE (Kaffe.Beskrivelse LIKE '%{beskrivelse}%')
                    UNION
                    SELECT Brenneri.Navn as BrenneriNavn, Kaffe.Navn as KaffeNavn FROM Kaffe 
                    INNER JOIN Brenneri on Kaffe.BrenneriId = Brenneri.BrenneriId
                    JOIN Kaffesmaking on Kaffe.KaffeId = Kaffesmaking.KaffeId
                    WHERE Kaffesmaking.Smaksnotat like '%{beskrivelse}%'

                    """)
    print(" ")
    print("Resultater: ")
    result = cursor.fetchall()
    tabell = []
    for x in result:
        insert = [x[0], x[1]]
        tabell.append(insert)
    for rad in tabell:
        print("{: >25} {: >20}".format(*rad))

def FemteBrukerHistorie():
    print("under produskjon 4")
    beskrivelse = input("Hvilket ord skal kaffens behandlingsmetode ikke bli beskrivet med? ")
    cursor.execute(f"""SELECT Brenneri.Navn as BrenneriNavn, Kaffe.Navn as KaffeNavn FROM Kaffe 
                    INNER JOIN Brenneri on Kaffe.BrenneriId = Brenneri.BrenneriId
                    INNER JOIN Kaffeparti on Kaffe.KaffepartiId = Kaffeparti.KaffepartiId
                    INNER JOIN Behandlingsmetode on Behandlingsmetode.BehandlingsId = Kaffeparti.BehandlingsId
                    WHERE (Behandlingsmetode.Beskrivelse NOT LIKE '%{beskrivelse}%')""")
    print(" ")
    print("Resultater: ")
    result = cursor.fetchall()
    tabell = []
    for x in result:
        insert = [x[0], x[1]]
        tabell.append(insert)
    for rad in tabell:
        print("{: >25} {: >20}".format(*rad))
    
    
def velgHistorie():
    val = input("Hvilken brukerhistorie vil du se? (Dette er i tall mellom 1 og 5) ")

    if val == "1":
        FørsteBrukerHistorie()
    elif val == "2":
        AndreBrukerHistorie()
    elif val == "3":
        TredjeBrukerHistorie()
    elif val == "4":
        FjerdeBrukerHistorie()
    elif val =="5":
        FemteBrukerHistorie()
    else:
        print("Dette er ugyldig brukerhistorie. Skriv inn riktig tall mellom 1 og 5")
        velgHistorie()


print("Velkommen til vårt kaffeprogram!")
velgHistorie()

