from datetime import date
from json.tool import main
import sqlite3

#Her lager vi connection
con = sqlite3.connect("kaffe.db")
cursor = con.cursor()

def lagBruker():
    print("""Under kommer felt du må fylle ut for å lage en bruker: 
        """)
    epost = input("Skriv inn din e-post?: ")
    passord = input("Skriv inn ønsket passord: ")
    fulltnavn = input("Skriv inn ditt fulle navn(Kan være blank): ")
    try:


        cursor.execute(f'''INSERT INTO Bruker
                VALUES ("{epost}", "{passord}", "{fulltnavn}")''')

        con.commit()

        cursor.execute(f'''SELECT Bruker.Epost, Bruker.FulltNavn FROM Bruker
                        WHERE Bruker.Epost Like "{epost}"''')
        
        res = cursor.fetchall()
        result = res[0]
        print(f"""
Du har nå laget en bruker med eposten: '{result[0]}'.
Passordet ditt er: ***** (Dette er hemmelig dessverre så håper du husker)
Ditt fulle navn er: {result[1]}.
            """)
        velgHistorie()
    except:
        print("Du har skrevet inn en allerede eksisterende bruker. Bruk en annen epost og prøv på nytt.")
        lagBruker()

def getBrenneriId(brenneri):
    try:
        cursor.execute(f"""SELECT BrenneriId from Brenneri 
                        WHERE Brenneri.Navn like '{brenneri}'
                    """)
        result = cursor.fetchone()
        return  result[0]
    except:
        print("Brennerinavnet er ikke i databasen, sender deg tilbake til starten.")
        FørsteBrukerHistorie()

def getKaffeId(kaffe, brenneriId):
    try:
        cursor.execute(f"""SELECT KaffeId from Kaffe 
                            INNER JOIN Brenneri on Brenneri.BrenneriId = Kaffe.BrenneriId
                            WHERE Kaffe.Navn like '{kaffe}' AND Brenneri.BrenneriId = {brenneriId}""")
        result = cursor.fetchone()
        return result[0]
    except:
        print("Kaffenavnet er enten ikke i databasen, eller så har brenneriet du skrev ikke laget en kaffe kalt dette, sender deg tilbake til starten.")
        FørsteBrukerHistorie()

def skrivNotat(epost, kaffeId, poeng, notat):
    try:
        datoStreng = date.today().isoformat()
        dato = datoStreng.split("-")
        år = int(dato[0])
        måned = int(dato[1])
        dag = int(dato[2])

        cursor.execute(f'''INSERT INTO Kaffesmaking (Smaksnotat, Poeng, BrukerId, År, Måned, Dag , KaffeId)
                VALUES ("{notat}", {poeng}, "{epost}", {år}, {måned}, {dag},{kaffeId})''')
                #VALUES ("TESTINPUT", 5, test@test.test, 2022, 03, 25, 1)''')
                #jobba litt, men ble trøtt. Det som mangler her er å få til å 
                #gjøre om datetime objekter til integers sånn at vi kan bruke dem
        con.commit()
    except:
        print("Obs, her skjedde det en feil, prøv på nytt")
        FørsteBrukerHistorie()

def printResultat():
    try:
        cursor.execute(f'''SELECT Kaffe.Navn, Brenneri.Navn,  Smaksnotat, Poeng, Bruker.FulltNavn, Dag, Måned, År From Kaffesmaking
                        JOIN Kaffe on Kaffe.KaffeId = Kaffesmaking.KaffeId
                        JOIN Bruker on Bruker.Epost = Kaffesmaking.BrukerId
                        JOIN Brenneri on Brenneri.BrenneriId = Kaffe.BrenneriId
                        ORDER by Kaffesmaking.KaffesmakingId DESC LIMIT 1
                        ''')
        res = cursor.fetchall()
        result = res[0]
        print(f"""
Du har nå ført inn et smaksnotat på kaffen '{result[0]}' fra {result[1]}.
Den ble skrevet av {result[4]} den {result[5]}. i {result[6]}. {result[7]}
Du ga den karakter {result[3]}/10 og skrev dette om den:
'{result[2]}'
            """)
    except:
        print("Noe gikk galt i spørringen, dette er ikke din feil. ")
    
    
    
    


def FørsteBrukerHistorie():
    epost = input("Hva er E-posten din? ")
    passord = input("Hva er passordet ditt? ")
    cursor.execute("""SELECT * FROM Bruker""")
    result = cursor.fetchall()
    b = False
    for x in result:
        if(epost == x[0] and passord == x[1]):
            b=True
    if(b):
        print("Du er logget inn")
    else:
        print("Feil brukernavn eller passord\nDu må skrive det inn på nytt")
        FørsteBrukerHistorie()



    brenneri = input("Hvilket brenneri er kaffen fra? ")
    brenneriId = getBrenneriId(brenneri)

    kaffe = input("Hva er Kaffens navn? ")
    kaffeId = getKaffeId(kaffe, brenneriId)

    poeng = input("Hvor mange poeng av 10 vil du gi den? ")
    notat = input("Skriv ned noen tanker om kaffen: ")


    skrivNotat(epost, kaffeId, poeng, notat)
    printResultat()



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
    val = input("Hvilken brukerhistorie vil du se? (Dette er i tall mellom 1 og 5 i listen over) ")

    if val == "0":
        lagBruker()
    elif val == "1":
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
        print("Dette er ugyldig brukerhistorie. Skriv inn riktig tall mellom 0 og 5")
        velgHistorie()


print("""
Velkommen til vårt kaffeprogram!""")
print("""
Under vil du finne en liste som vil gi deg alternativer for søk
""")
print("""
0. tast 0 om du vil lage en bruker?
1. Ønsker du å lage ett nytt smaksnotat?
2. Statistikk om hvem som har drukket mest kaffe
3. Finne kaffen med mest verdi for pengene
4. Søke etter kaffe med spesifikk beskrivelse (i enkelt ord)
5. Finne kaffe som ikke innheolder behandlingsmetoden du vil unngå
""")
velgHistorie()

