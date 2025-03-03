# %% [markdown]
# # Werkcollege-opdrachten Week 1.1

# %% [markdown]
# ## Maak een virtual environment

# %% [markdown]
# Zorg dat je met behulp van de handleiding *Bouw en gebruik van virtual environments - Handleiding* een virtual environment hebt gemaakt, dat jou en je duopartner garandeert altijd dezelfde versie van geïmporteerde dependencies te gebruiken.<br>
# Voeg hier vervolgens met *poetry add pandas* de pandas-dependency aan toe.<br>
# Als je dit allemaal goed hebt gedaan moet de onderstaande code bij jullie allebei succesvol runnen:

# %%
import pandas as pd

# %% [markdown]
# Zorg er daarnaast voor dat je...
# - Het bestand Waarheidstabel.png in dezelfde map als dit notebook hebt staan.
# - Het bestand Prinstabel.png in dezelfde map als dit notebook hebt staan.
# - Alle informatie onder het kopje *Basisoperaties* van de cheatsheet *Van Java naar Python - Cheatsheet* (zie Brightspace) bij de hand hebt.

# %% [markdown]
# ## 1.1: Output, variabelen en input

# %% [markdown]
# Geef code waarmee het volgende op het scherm komt te staan:<br>
# geef me je geld <br>
# of ik gebruik geweld, <br>
# toen kwam de controle aangesneld

# %%
print("geef me je geld\nof ik gebruik geweld,\ntoen kwan de controle aangesneld")

# %% [markdown]
# Declareer 2 variabelen zodat de volgende tekst geprint wordt:<br>
# Apenhoofd<br>
# Paardenstaart

# %%
string1 = 'Apenhoofd'
string2 = 'Paardenstaart'

print(string1 + '\n' + string2)

# %% [markdown]
# Voeg code toe zodat het programma het volgende doet:<br>
# 1): Op het scherm komt A, B, C, D, ..., F, G te staan<br>
# 2): De gebruiker voert een letter in<br>
# 3): Op het scherm komt te staan:<br>
# Het is inderdaad:<br>
# *ingevoerde letter*

# %%
character = input("A, B, C, D, ..., F, G")
print("Het is inderdaad " + character if character == "E" else "Het is niet " + character)

# %% [markdown]
# ## 1.2: Stringconcatenatie en Rekenen

# %% [markdown]
# Schrijf code dat een inkomen inleest en het volgende uitprint:<br>
# Uw inkomen (*ingelezen inkomen*) is zeer acceptabel.

# %%
print(f"Uw inkomen {int(input())} is zeer acceptabel.")

# %% [markdown]
# De oppervlakte van een driehoek is 1/2 * hoogte * basis<br>
# Schrijf code zodat het programma het volgende doet:<br>
# 1): Op het scherm komt Wat is de basis? te staan<br>
# 2): De gebruiker voert een basis in<br>
# 3): Op het scherm komt Wat is de hoogte? te staan<br>
# 4): De gebruiker voert een hoogte in<br>
# 5): Op het scherm komt: De oppervlakte van de driehoek is *berekende oppervlakte* te staan

# %%
print(f"De oppervlakte van de driehoek is: {(1/2)*int(input("Wat is de basis?"))*int(input("Wat is de hoogte?"))}")

# %% [markdown]
# ## 1.3: if() en booleans

# %% [markdown]
# Schrijf code dat het volgende doet:<br>
# 1): De gebruiker voert in hoe oud iemand is<br>
# 2): De gebruiker voert in of de ouders meegekomen zijn (input is J of N)<br><br>
# 
# Als...
# - Jonger dan 6, wel ouders: op het scherm staat Je mag het zwembad in
# - Jonger dan 6, geen ouders: op het scherm staat Je mag het niet zwembad in
# - Leeftijd vanaf 6, geen ouders: op het scherm staat Je mag het zwembad in als je een diploma hebt
# - Leeftijd vanaf 6, wel ouders: op het scherm staat Waarom neem je nog je ouders mee?

# %%
leeftijd = int(input("Wat is de leeftijd?"))
ouders_mee = input("Zijn de ouders meegekomen? [J/N]: ").strip().upper() == "J"

print(
    "Je mag het zwembad in" if leeftijd < 6 and ouders_mee else
    "Je mag het niet zwembad in" if leeftijd < 6 else
    "Je mag het zwembad in als je een diploma hebt" if not ouders_mee else
    "Waarom neem je nog je ouders mee?"
)

# %% [markdown]
# Schrijf code zodat de boolean-variabelen een en twee aangemaakt worden en waarmee de juiste waarde in de boolean-variabele uitkomst komt te staan. In de waarheidstabel hieronder staat wat de waarde van uitkomst is bij de verschillende mogelijke combinaties van een en twee.<br><br>
# <img src="Waarheidstabel.png">

# %%
print("Onwaar" if int(input("Een")) and not int(input("Twee")) else "Waar")

# %% [markdown]
# ## 1.4: Methoden

# %% [markdown]
# Schrijf een methode wachtwoord die als parameters twee woorden meekrijgt en het volgende controleert:
# - Als de woorden gelijk zijn, print het programma gelijk.
# - Als de woorden ongelijk zijn print het programma ongelijk.
# 
# Vergeet niet dat je de methode niet alleen aan moet maken, maar ook aan moet roepen om output te krijgen.

# %%
def wachtwoord(woord1, woord2):
    print("Gelijk" if woord1 == woord2 else "Ongelijk")

wachtwoord(input(), input())

# %% [markdown]
# Schrijf de methode zoekPrins die als parameter een prinses meekrijgt en vervolgens de bijbehorende prins teruggeeft, volgens de volgende tabel:<br><br>
# <img src="Prinstabel.png"><br>
# Als de naam van de prinses niet in de tabel staat wordt het volgende door de methode teruggegeven: naamloos.<br>
# Roep ten slotte de gemaakte methode ook daadwerkelijk aan met een zelfgekozen prinsessennaam.

# %%
couples = {
    "Aurora" : "Philip", 
    "Ariel" : "Eric", 
    "Jasmine" : "Aladdin", 
    "Pocahontas" : "John", 
    "Belle" : "Beast", 
    "Tiana" : "Naveen",
    "Mulan" : "Shang"
}

def zoekPrins(prinsess):
    print(couples[prinsess] if prinsess in couples else "naamloos")

zoekPrins(input())

# %% [markdown]
# ## 1.5: While

# %% [markdown]
# Schrijf de inhoud van de methode wachtwoord. Deze heeft geen parameters en laat de gebruiker twee wachtwoorden invoeren, waarna hij bekijkt of deze gelijk zijn. Zolang dat niet het geval is wordt er eerst Fout, probeer het opnieuw! uitgeprint en moet de gebruiker het opnieuw proberen.<br>Als de gebruiker het goed doet, komt er Succes! op het scherm te staan.

# %%
while (a := input()) != (b := input()):
    print("Fout, probeer het opnieuw!")
print("Success!")

# %% [markdown]
# Schrijf de inhoud van de methode tafels. De methode print alle tafels vanaf 1 (dus inclusief de tafel van 1) tot en met de tafel van het meegekregen getal (dus inclusief de tafel van getal).  Zet een witregel tussen alle tafels in. <br>
# Let op:
# - Gebruik een while-loop
# - Gebruik de reeds geschreven methode tafel om een tafel uit te printen

# %%
def tafel(getal: int):
    teller: int = 1

    while teller <= 10:
        print(f'{teller} x {getal} = {teller * getal}')
        teller += 1

def tafels(getal: int):
    teller: int = 1

    while teller <= getal:
        print(tafel(teller))
        teller += 1 

x: int = int(input())
tafels(x)

# %% [markdown]
# ## For-loop

# %% [markdown]
# Vervang de while-loop door een werkende for-loop. De uitkomst van het programma mag daarbij niet veranderen.

# %%
def loopje():
    for x in range(11):
        print(f"huidige getal: {x}")

loopje()

# %% [markdown]
# Schrijf de methode checkEven die achtereenvolgens 12 getallen inleest en afdrukt hoe vaak het ingevoerde getal even was.

# %%
def checkEven():
    teller = 0
    for x in range(12):
        if int(input()) % 2 == 0:
            teller += 1
    print(teller)

checkEven()

# %% [markdown]
# ## Objectoriëntatie

# %% [markdown]
# Maak een minisysteem voor een kledingwinkel. Maak verschillende klassen voor verschillende soorten kledingstukken, waarbij sommige klassen geërfd worden van andere klassen.
# - Maak een klasse Kledingstuk aan, waarin door de constructor een merk, een maat en een prijs geïnitialiseerd worden.
# - Maak een klasse Broek en een klasse Shirt, beide erven van de klasse Kledingstuk. Voeg aan Broek een broek_type, en aan Shirt een shirt_type toe (d.m.v. constructorgebruik).
# - Maak een klasse Spijkerbroek die erft van broek en een klasse Poloshirt die erft van shirt. Voeg aan Spijkerbroek een blauwtint toe, en aan Poloshirt een kraagsoort (d.m.v. constructorgebruik).
# - Implementeer in elke klasse een beschrijf-methode, waarmee alle informatie over het betreffende kledingstuk wordt afgedrukt.
# - Maak van elke klasse een object aan en roep de beschrijfmethode aan. Controleer nauwkeurig of alles naar behoren werkt.

# %%
class Kledingstuk:

    def __init__(self, merk, maat, prijs):
        self.merk = merk
        self.maat = maat
        self.prijs = prijs

class Broek(Kledingstuk):

    def __init__(self, merk, maat, prijs, broekType):
        self.broekType = broekType
        super().__init__(merk, maat, prijs)

class Spijkerbroek(Broek):

    def __init__(self, merk, maat, prijs, broekType, blauwtint):
        self.blauwtint = blauwtint
        super().__init__(merk, maat, prijs, broekType)

class Shirt(Kledingstuk):

    def __init__(self, merk, maat, prijs, shirtType):
        self.shirtType = shirtType
        super().__init__(merk, maat, prijs)

class Poloshirt(Shirt):

    def __init__(self, merk, maat, prijs, shirtType, kraagsoort):
        self.kraagsoort = kraagsoort
        super().__init__(merk, maat, prijs, shirtType)

k1 = Kledingstuk("Adidas", 32, 100.00)
b1 = Broek("Floris Duetz", 34, 120.00, "Chino")
b2 = Spijkerbroek("Vanguard", 34, 110.00, "Spijkerbroek", "Navy")
s1 = Shirt("Slater", 38, 20.00, "T-shirt")
s2 = Poloshirt("Lacoste", 38, 30.00, "Poloshirt", "Kent kraag")

kleding = [k1, b1, b2, s1, s2]

for x in kleding:
    print(vars(x))

# %% [markdown]
# Opmerking: in themaweken 2 t/m 8 ga je objectoriëntatie waarschijnlijk veel minder vaak gebruiken dan de andere boven- en ondergenoemde programmeertechnieken.<br>
# Maar let op: in themaweken 9 en 10 komt objectoriëntatie <b><u>uitvoerig</u></b> aan de orde. Zorg dus dat je deze kennis niet vergeet!

# %% [markdown]
# ## Verzamelingen

# %% [markdown]
# Kijk nu naar alle info onder het kopje *Verzamelingen* van de cheatsheet *Van Java naar Python - Cheatsheet*.

# %% [markdown]
# Initialiseer een lijst met de naam mijn_lijst met de volgende waarden:<br>
# Jelle, Marleen, Henk, Fatima, Jelle, Henk

# %%
mijn_lijst = ["Jelle", "Marleen", "Henk", "Fatima", "Jelle", "Henk", ]

# %% [markdown]
# Probeer nu de eerste waarde uit te lijst te veranderen in een naam naar keuze. Lukt dat?

# %%
print(mijn_lijst[0])
mijn_lijst[0] = input()
print(mijn_lijst[0])

# %% [markdown]
# Maak van bovengenoemde lijst nu een tupel, genaamd: mijn_tupel.

# %%
mijn_tupel = (1, 2, 3, 4, 5)

# %% [markdown]
# Probeer nu de eerste waarde uit te tupel te veranderen in een naam naar keuze. Lukt dat?

# %%
print(mijn_tupel)

mijn_lijst = list(mijn_tupel)

mijn_lijst[0] = "Banaan"

mijn_tupel = tuple(mijn_lijst)
print(mijn_tupel)

# %% [markdown]
# Initialiseer een dictionary met de volgende key-value-combinaties:
# - naam: "Jelle"
# - leeftijd: 28
# - beroep: "Docent"
# - hobby: "Volleybal"

# %%
dic = {"naam" : "Jelle", "leeftijd" : 28, "beroep" : "Docent", "hobby" : "Volleyball", }

# %% [markdown]
# Probeer nu de naam te veranderen naar een naam naar keuze. Lukt dat?

# %%
dic = {"naam" : "Jelle", "leeftijd" : 28, "beroep" : "Docent", "hobby" : "Volleyball", }

dic["naam"]  = "Mark"
print(dic["naam"])


