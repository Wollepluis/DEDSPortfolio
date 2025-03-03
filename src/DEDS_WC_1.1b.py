# %% [markdown]
# # Werkcollege-opdrachten Week 1.2

# %% [markdown]
# ## Voorbereiding

# %% [markdown]
# Importeer in het codeblok hieronder de packages die worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
# N.B.: de 2 reeds geschreven coderegels zorgen ervoor dat eventuele warnings, die code-outputs lelijker maken, uitgezet worden.

# %%
import warnings
warnings.simplefilter('ignore')
import pandas as pd
import sqlite3

# %% [markdown]
# Zet de volgende bestanden in een makkelijk terug te vinden map:
# - go_sales_train.sqlite
# - go_crm_train.sqlite
# - go_staff_train.sqlite

# %% [markdown]
# Bestudeer de bovenste 3 bestanden in DB Browser (SQLite), <a href="https://sqlitebrowser.org/dl/">hier</a> te downloaden. Wat valt je op qua datatypen?<br>

# %% [markdown]
# ## Databasetabel inlezen

# %% [markdown]
# Creëer een databaseconnectie met het bestand go_sales_train.sqlite.

# %%
conn = sqlite3.connect("../Data/Week1/go_sales_train.sqlite")
print(conn)

# %% [markdown]
# <b>Let goed op:</b><br>
# Als je per ongeluk een verkeerde bestandsnaam ingeeft, maakt Python zélf een leeg databasebestand aan! Er ontstaat dan dus een nieuwe .sqlite, en dat is nadrukkelijk <u>niet de bedoeling.</u>

# %% [markdown]
# Gebruik de onderstaande sql_query om te achterhalen welke databasetabellen in go_sales_train zitten.

# %%
sql_query = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
sql_query
#Vul dit codeblok verder in

# %% [markdown]
# Krijg je lege output? Dan heb je per ongeluk een leeg  databasebestand (.sqlite) aangemaakt.<br>
# Lees de informatie onder het kopje <u>Let goed op:</u> hierboven nog eens goed door.

# %% [markdown]
# Gebruik de gecreëerde databaseconnectie om de resultaten van de volgende query in een DataFrame te zetten:<br>
# *SELECT * FROM sales_staff* 

# %%
sql_query = "SELECT * FROM sales_staff"
data_frame = pd.read_sql(sql_query, conn)

data_frame

# %% [markdown]
# ## Datumkolommen

# %% [markdown]
# Zoals je misschien al hebt gezien in DB Browser, zijn datums als TEXT opgeslagen, en niet als DATE, DATETIME o.i.d. Hier moeten we dus nog even "typische datumkolommen" van maken. Dat doen we met de volgende code:

# %%
data_frame['DATE_HIRED'] = pd.to_datetime(data_frame['DATE_HIRED'])
data_frame.dtypes

# %% [markdown]
# Als we hier het jaar uit willen halen, schrijven we:

# %%
data_frame['DATE_HIRED'].dt.year

# %% [markdown]
# Deze zelfde syntax is te gebruiken voor het extraheren van kwartalen, maanden, weken en dagen. Probeer het maar eens!

# %% [markdown]
# ## DataFrames uitsplitsen en opbouwen met Series

# %% [markdown]
# De volgende 5 kolommen hebben betrekking op de contactdetails van elke medewerker in dit DataFrame:
# - SALES_STAFF_CODE
# - WORK_PHONE
# - EXTENSION
# - FAX
# - EMAIL
# 
# Maak van elk van deze 5 kolommen een serie.

# %%
sales_staff_codeSerie = data_frame['SALES_STAFF_CODE']
work_phoneSerie = data_frame['WORK_PHONE']
extensionSerie = data_frame['EXTENSION']
faxSerie = data_frame['FAX']
emailSerie = data_frame['EMAIL']

# %% [markdown]
# Zet allevijf gecreëerde series als kolommen naast elkaar in een DataFrame (*contact_details*). Gebruik pd.concat(...)<br>
# Hulpvraag: welke waarde geef je aan de axis-parameter?

# %%
modified_Dataframe = pd.concat([sales_staff_codeSerie, work_phoneSerie, extensionSerie, faxSerie, emailSerie], axis=1)
modified_Dataframe

# %% [markdown]
# ## Series en DataFrames maken vanuit lists en dictionaries

# %% [markdown]
# Met .head(*getal*) kan je de bovenste *getal* rijen van een tabel selecteren.<br>
# Selecteer op deze manier de bovenste 5 rijen van *contact_details*.<br>
# Sla dit resultaat op in een nieuw DataFrame.

# %%
modified_Dataframe2 = modified_Dataframe
modified_Dataframe2.head(5)

# %% [markdown]
# Aan deze 10 rijen met contactdetails willen we 3 kolommen toevoegen: 'FIRST_LANGUAGE', 'SECOND_LANGUAGE' & 'THIRD_LANGUAGE'.<br>
# Iedereens 'First Language' is Engels, afgekort 'EN'. Maak een lijst waarin 5x 'EN' staat.<br>
# Converteer deze lijst vervolgens naar een serie en voeg deze horizontaal samen met het resultaat van de vorige opdracht.<br>
# Vergeet niet een passende naam te geven aan de nieuw ontstane kolom.

# %%
language_list = ['EN', 'EN', 'EN', 'EN', 'EN']

first_languageSerie = pd.Series(language_list, name='FIRST_LANGUAGE')

modified_Dataframe2 = pd.concat([modified_Dataframe2, first_languageSerie], axis=1)
modified_Dataframe2.head(5)

# %% [markdown]
# Maak nu de tweede kolom ('SECOND_LANGUAGE'). Maak daarvoor een dictionary, met daarin...
# - Als keys: alle indexen uit het resultaat van het vorige codeblok.
# - Als values: bij de eerste 3 elementen 'FR' (Frankrijk), bij de laatste 2 'DE' (Duitsland).
# 
# Maak vervolgens ook hier weer een serie van en voeg ook deze weer horizontaal samen met het rsultaat van de vorige opdracht.<br>
# Vergeet niet een passende naam te geven aan de nieuw ontstane kolom.

# %%
language_dic = {0 : 'FR', 1 : 'FR', 2 : 'FR', 3 : 'DE', 4 : 'DE'}

second_languageSerie = pd.Series(language_dic, name='SECOND_LANGUAGE')

modified_Dataframe2 = pd.concat([modified_Dataframe2, second_languageSerie], axis=1)
modified_Dataframe2.head(5)

# %% [markdown]
# Maak ten slotte de derde kolom ('THIRD_LANGUAGE') door een dictionary te maken met daarin...
# - Als key: de naam van de nieuwe kolom. Zie je het verschil qua keys met de vorige opdracht?
# - Als waarde: een lijst met daarin 'NL', 'NL', 'JPN', 'JPN', 'KOR'.
# 
# Converteer deze dictionary nu naar een DataFrame en voeg deze horizontaal samen met het resultaat van de vorige opdracht.<br>
# Waarom hoef je hierna de nieuw ontstane kolom geen passende naam meer te geven?

# %%
language_dic = {'THIRD_LANGUAGE': ['NL', 'NL', 'JPN', 'JPN', 'KOR']}
third_language_df = pd.DataFrame(language_dic)
modified_Dataframe2 = pd.concat([modified_Dataframe2, third_language_df], axis=1)

modified_Dataframe2.head(5)

# %% [markdown]
# ## Data toevoegen

# %% [markdown]
# ### Rijen

# %% [markdown]
# Gebruik de originele databasetabel *sales_staff*.<br>
# Voeg een extra rij toe met eigen invulling. Zorg ervoor dat de index netjes doorloopt.<br>
# Hulpvraag: welke waarde geef je nu aan axis?

# %%
sql_query = "SELECT * FROM sales_staff"
data_frame = pd.read_sql(sql_query, conn)

new_row = {
    'SALES_STAFF_CODE': 6969,
    'FIRST_NAME': 'Mark',
    'LAST_NAME': 'Wilbrink',
    'POSITION_EN': 'Sales Manager',
    'WORK_PHONE': '+1234567890',
    'EXTENSION': 123,
    'FAX': '+1234567890',
    'EMAIL': 'Mark@gmail.com',
    'DATE_HIRED': '1970-10-11',
    'SALES_BRANCH_CODE': 6
}

new_row_df = pd.DataFrame([new_row])

updated_data_frame = pd.concat([data_frame, new_row_df], ignore_index=True)

updated_data_frame.tail(5)

# %% [markdown]
# ### Kolommen

# %% [markdown]
# Voeg een kolom *FULL_NAME* toe die de waarden van *FIRST_NAME* en *LAST_NAME* achter elkaar zet, gescheiden door een spatie.

# %%
data_frame['FULL_NAME'] = data_frame['FIRST_NAME'] + ' ' + data_frame['LAST_NAME']
data_frame.head(5)

# %% [markdown]
# ## Data wijzigen

# %% [markdown]
# ### Datatypen

# %% [markdown]
# Door het attribuut .dtypes van een DataFrame op te vragen krijg je een serie die per kolom het datatype weergeeft. Doe dit bij de originele databasetabel *sales_staff*

# %%
sql_query = "SELECT * FROM sales_staff"
data_frame = pd.read_sql(sql_query, conn)

data_frame.dtypes

# %% [markdown]
# Hier valt op dat elke kolom het datatype 'object' heeft: Python leest dus alles als string. Wiskundige operaties zijn hierdoor niet mogelijk.<br>
# We kunnen proberen om kolommen met getallen, bijvoorbeeld de 'extension', te converteren naar een int. Zie onderstaande code.

# %%
data_frame['EXTENSION'] = data_frame['EXTENSION'].astype(int)
data_frame.dtypes

# %% [markdown]
# Dit lukt echter niet, omdat er in de kolom 'EXTENSION' lege waarden zitten die niet geconverteerd kunnen worden naar een int.<br>
# Wél kan je deze naar een float converteren, zie onderstaande code:

# %%
data_frame['EXTENSION'] = data_frame['EXTENSION'].astype(float)
data_frame.dtypes

# %% [markdown]
# Als we in de rij van 'EXTENSION' kijken zien we dat de conversie van het datatype nu is gelukt.<br>
# Dit is <b>randvoorwaardelijk</b> voor het uitvoeren van wiskundige operaties.<br>

# %% [markdown]
# ### Rijen

# %% [markdown]
# Zorg er nu voor dat bij alle extensions 1 wordt opgeteld.

# %%
data_frame['EXTENSION'] += 1
data_frame

# %% [markdown]
# Elke 'Branch Manager' wordt nu 'General Manager'. Schrijf code zodat deze wijziging doorgevoerd wordt in het DataFrame.

# %%
data_frame.loc[data_frame['POSITION_EN'] == 'Branch Manager', 'POSITION_EN'] = 'General Manager'
data_frame

# %% [markdown]
# ### Kolommen

# %% [markdown]
# Verander de kolomnaam 'POSITION_EN' naar 'POSITION'.

# %%
data_frame.rename(columns={'POSITION_EN': 'POSITION'}, inplace=True)
data_frame


# %% [markdown]
# ## Data verwijderen

# %% [markdown]
# ### Rijen

# %% [markdown]
# De medewerkers op indexen 99, 100 en 101 hebben helaas ontslag genomen.<br>
# Verwijder de bijbehorende rijen uit het DataFrame. Gebruik slechts één keer de .drop()-methode.

# %%
data_frame.drop([99, 100, 101], inplace=True)
data_frame

# %% [markdown]
# ### Kolommen

# %% [markdown]
# Faxen zijn inmiddels ouderwets: niemand gebruikt zijn/haar faxnummer nog.<br>
# Verwijder de bijbehorende kolom uit het DataFrame.

# %%
data_frame.drop(columns=['FAX'], inplace=True)
data_frame


