# %% [markdown]
# # Werkcollege-opdrachten Week 1.3

# %% [markdown]
# ## Dependencies importeren

# %% [markdown]
# Kopieer in het codeblok hieronder van het vorige practicum de import-code voor de dependencies die het vaakst worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
# Zet eventuele warnings uit.

# %%
import warnings
warnings.simplefilter('ignore')
import pandas
import sqlite3

# %% [markdown]
# Zet het bestand go_sales_train.sqlite in een makkelijk te vinden map

# %% [markdown]
# ## Databasetabellen inlezen

# %% [markdown]
# Kopieer in het codeblok hieronder van het vorige practicum de code om een connectie met het bestand go_sales_train.sqlite te maken.

# %%
conn = sqlite3.connect("../Data/Week1/go_sales_train.sqlite")
print(conn)

# %% [markdown]
# Lees van de ingelezen go_sales_train-database te volgende tabellen in met behulp van "SELECT * FROM *tabel*".
# - product
# - product_type
# - product_line
# - sales_staff
# - sales_branch
# - retailer_site
# - country
# - order_header
# - order_details
# - returned_item
# - return_reason

# %%
tables_query = "SELECT name FROM sqlite_master WHERE type= 'table';"
tables = pandas.read_sql(tables_query, conn)

df = {}

for table_name in tables['name']:
    query = f"SELECT * FROM {table_name}"
    df[table_name] = pandas.read_sql(query, conn)

def get_table_data(table_names):
    
    if isinstance(table_names, str):
        table_names = [table_names]

    tables = [df.get(name, pandas.DataFrame()) for name in table_names]

    if not tables:
        print(f"None of the specified tables were found.")
        return pandas.DataFrame()

    merged_data = merge_table_data(tables)
    return merged_data

def merge_table_data(tables):
    merged_data = tables[0]

    for current_table in tables[1:]:
        common_columns = merged_data.columns.intersection(current_table.columns)

        if not common_columns.empty:
            merge_column = common_columns[0]
            merged_data = pandas.merge(merged_data, current_table, on=merge_column, how='inner')
        else:
            print(f"No common column found between the tables")

    return merged_data

# %% [markdown]
# Krijg je een "no such table" error? Dan heb je misschien met .connect() per ongeluk een leeg  databasebestand (.sqlite) aangemaakt. <u>Let op:</u> lees eventueel de informatie uit het Notebook van werkcollege 1.1b nog eens goed door.

# %% [markdown]
# Als je tijdens onderstaande opdrachten uit het oog verliest welke tabellen er allemaal zijn, kan je deze Pythoncode uitvoeren:

# %%
sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
#Vul dit codeblok verder in
pandas.read_sql(sql_query, conn)
#Op de puntjes hoort de connectie naar go_sales_train óf go_staff_train óf go_crm_train te staan.

# %% [markdown]
# erachter 

# %% [markdown]
# Let op! Voor alle onderstaande opdrachten mag je <u>alleen Python</u> gebruiken, <u>geen SQL!</u>

# %% [markdown]
# ## Selecties op één tabel zonder functies

# %% [markdown]
# Geef een overzicht met daarin de producten en hun productiekosten waarvan de productiekosten lager dan 100 dollar en hoger dan 50 dollar ligt. (2 kolommen, 23 rijen)

# %%
table_data = get_table_data('product')

filter = (table_data['PRODUCTION_COST'] > 50) & (table_data['PRODUCTION_COST'] < 100)
table_data.loc[filter, ['PRODUCT_NAME', 'PRODUCTION_COST']]

# %% [markdown]
# Geef een overzicht met daarin de producten en hun marge waarvan de marge lager dan 20 % of hoger dan 60 % ligt. (2 kolommen, 7 rijen) 

# %%
filter = (table_data['MARGIN'] < 0.20) | (table_data['MARGIN'] > 0.60)
table_data.loc[filter, ['PRODUCT_NAME', 'MARGIN']]

# %% [markdown]
# Geef een overzicht met daarin de landen waar met francs wordt betaald. Sorteer de uitkomst op land.  (1 kolom, 3 rijen)

# %%
table_data = get_table_data('country')

filter = table_data['CURRENCY_NAME'] == 'francs'
table_data.loc[filter, ['COUNTRY']]

# %% [markdown]
# Geef een overzicht met daarin de verschillende introductiedatums waarop producten met meer dan 50% marge worden geïntroduceerd (1 kolom, 7 rijen) 

# %%
table_data = get_table_data('product')

filter = table_data['MARGIN'] > 0.50
table_data.loc[filter, ['INTRODUCTION_DATE']].drop_duplicates('INTRODUCTION_DATE')

# %% [markdown]
# Geef een overzicht met daarin het eerste adres en de stad van verkoopafdelingen waarvan zowel het tweede adres als de regio bekend is (2 kolommen, 7 rijen)

# %%
table_data = get_table_data('sales_branch')

filter = table_data['REGION'].notna() & table_data['ADDRESS2'].notna()
table_data.loc[filter, ['ADDRESS1', 'CITY']]

# %% [markdown]
# Geef een overzicht met daarin de landen waar met dollars (dollars of new dollar) wordt betaald. Sorteer de uitkomst op land. (1 kolom, 4 rijen) 

# %%
table_data = get_table_data('country')

filter = table_data['CURRENCY_NAME'].str.contains('dollar')
table_data.loc[filter, ['COUNTRY']].sort_values(by='COUNTRY', ascending=True)

# %% [markdown]
# Geef een overzicht met daarin beide adressen en de stad van vestigingen van klanten waarvan de postcode begint met een ‘D’ (van duitsland). Filter op vestigingen die een tweede adres hebben. (3 kolommen, 2 rijen) 

# %%
table_data = get_table_data('retailer_site')

filter = (table_data['POSTAL_ZONE'].str[0] == 'D') & table_data['ADDRESS2'].notna()
table_data.loc[filter, ['ADDRESS1', 'ADDRESS2', 'CITY']]

# %% [markdown]
# ## Selecties op één tabel met functies

# %% [markdown]
# Geef het totaal aantal producten dat is teruggebracht (1 waarde) 

# %%
table_data = get_table_data('returned_item')

print(table_data['RETURN_QUANTITY'].sum())

# %% [markdown]
# Geef het aantal regio’s waarin verkoopafdelingen gevestigd zijn. (1 waarde)

# %%
table_data = get_table_data('sales_branch')

print(table_data['REGION'].count())

# %% [markdown]
# Maak 3 variabelen:
# - Een met de laagste
# - Een met de hoogste
# - Een met de gemiddelde (afgerond op 2 decimalen)
# 
# marge van producten (3 kolommen, 1 rij) 

# %%
table_data = get_table_data('product')

lowest = table_data['MARGIN'].min()
highest = table_data['MARGIN'].max()
average = round(table_data['MARGIN'].mean(), 2)

frame = pandas.DataFrame({
    'lowest': [lowest],
    'highest': [highest],
    'average': [average]
})

frame

# %% [markdown]
# Geef het aantal vestigingen van klanten waarvan het 2e adres niet bekend is (1 waarde)

# %%
table_data = get_table_data('retailer_site')

filter = len(table_data['ADDRESS2'].isna())
filter

# %% [markdown]
# Geef de gemiddelde kostprijs van de verkochte producten waarop korting (unit_sale_price < unit_price) is verleend (1 waarde) 

# %%
table_data = get_table_data('order_details')

filter = table_data['UNIT_SALE_PRICE'].fillna(0) < table_data['UNIT_PRICE'].fillna(0)
avgUnitCost = table_data.loc[filter, 'UNIT_COST'].mean()
print(avgUnitCost)

# %% [markdown]
# Geef een overzicht met daarin het aantal medewerkers per medewerkersfunctie (2 kolommen, 7 rijen) 

# %%
table_data = get_table_data('sales_staff')

filter = table_data['POSITION_EN'].value_counts()
pandas.DataFrame(filter)

# %% [markdown]
# Geef een overzicht met daarin per telefoonnummer het aantal medewerkers dat op dat telefoonnummer bereikbaar is. Toon alleen de telefoonnummer waarop meer dan 4 medewerkers bereikbaar zijn. (2 kolommen, 10 rijen) 

# %%
table_data = get_table_data('sales_staff')

filter = table_data['WORK_PHONE'].value_counts()
pandas.DataFrame(filter[filter > 4])

# %% [markdown]
# ## Selecties op meerdere tabellen zonder functies

# %% [markdown]
# Geef een overzicht met daarin het eerste adres en de stad van vestigingen van klanten uit ‘Netherlands’ (2 kolommen, 20 rijen) 

# %%
table_data = get_table_data(['retailer_site', 'country'])

filter = table_data[table_data['COUNTRY'] == 'Netherlands']
filter[['ADDRESS1', 'CITY']]

# %% [markdown]
# Geef een overzicht met daarin de productnamen die tot het producttype ‘Eyewear’ behoren. (1 kolom, 5 rijen) 

# %%
table_data = get_table_data(['product_type', 'product'])

filter = table_data[table_data['PRODUCT_TYPE_EN'] == 'Eyewear']
pandas.DataFrame(filter['PRODUCT_NAME'])


# %% [markdown]
# Geef een overzicht met daarin alle unieke eerste adressen van klantvestigingen en de voornaam en achternaam van de verkopers die ‘Branch Manager’ zijn en aan deze vestigingen hebben verkocht (3 kolommen, 1 rij) 

# %%
# I don't snap

# %% [markdown]
# Geef een overzicht met daarin van de verkopers hun functie en indien zij iets hebben verkocht de datum waarop de verkoop heeft plaatsgevonden. Laat alleen de verschillende namen van de posities zien van de verkopers die het woord ‘Manager’ in hun positienaam hebben staan. (2 kolommen, 7 rijen) 

# %%
table_data = get_table_data(['order_header', 'sales_staff'])

filter = table_data[table_data['POSITION_EN'].str.contains('Manager', case=False)]
filter[['FIRST_NAME', 'ORDER_DATE']]

# %% [markdown]
# Geef een overzicht met daarin de verschillende namen van producten en bijbehorende namen van producttypen van de producten waarvoor ooit meer dan 750 stuks tegelijk verkocht zijn. (2 kolommen, 9 rijen) 

# %%
table_data = get_table_data(['product','order_details', 'product_type'])

filter = table_data[table_data['QUANTITY'] > 750]
pandas.DataFrame(filter[['PRODUCT_NAME', 'PRODUCT_TYPE_EN']].drop_duplicates())

# %% [markdown]
# Geef een overzicht met daarin de productnamen waarvan ooit meer dan 40% korting is verleend. De formule voor korting is: (unit_price - unit_sale_price) / unit_price (1 kolom, 8 rijen) 

# %%
table_data = get_table_data(['product', 'order_details'])

korting = ((table_data['UNIT_PRICE'] - table_data['UNIT_SALE_PRICE']) / table_data['UNIT_PRICE']) * 100

filter = table_data[korting > 40]
pandas.DataFrame(filter['PRODUCT_NAME'].drop_duplicates())

# %% [markdown]
# Geef een overzicht met daarin de retourreden van producten waarvan ooit meer dan 90% van de aangeschafte hoeveelheid is teruggebracht (return_quantity/quantity). (1 kolom, 3 rijen) 

# %%
table_data = get_table_data(['returned_item', 'order_details' , 'return_reason'])

formula = (table_data['RETURN_QUANTITY'] / table_data['QUANTITY']) * 100

filter = table_data[formula > 90]
pandas.DataFrame(filter['RETURN_DESCRIPTION_EN']).drop_duplicates()

# %% [markdown]
# ## Selecties op meerdere tabellen met functies

# %% [markdown]
# Geef een overzicht met daarin per producttype het aantal producten die tot dat producttype behoren. (2 kolommen, 21 rijen) 

# %%
table_data = get_table_data(['product', 'product_type'])

filter = table_data.groupby('PRODUCT_TYPE_EN')['PRODUCT_NUMBER'].count()
pandas.DataFrame(filter)

# %% [markdown]
# Geef een overzicht met daarin per land het aantal vestigingen van klanten die zich in dat land bevinden. (2 kolommen, 21 rijen) 

# %%
table_data = get_table_data(['retailer_site', 'country'])

filter = table_data.groupby('COUNTRY')['RETAILER_SITE_CODE'].count()
pandas.DataFrame(filter)

# %% [markdown]
# Geef een overzicht met daarin van de producten behorend tot het producttype ‘Cooking Gear’ per productnaam de totaal verkochte hoeveelheid en de gemiddelde verkoopprijs. Sorteer de uitkomst op totaal verkochte hoeveelheid. (4 kolommen, 10 rijen) 

# %%

table_data = get_table_data(['product', 'order_details', 'product_type'])
filtered_data = table_data[table_data['PRODUCT_TYPE_EN'] == 'Cooking Gear']

grouped_data = filtered_data.groupby('PRODUCT_NAME').agg(
    TOTAL_QUANTITY=('QUANTITY', 'sum'),
    AVERAGE_SALES_PRICE=('UNIT_SALE_PRICE', 'mean')
).reset_index()

pandas.DataFrame(grouped_data)



# %% [markdown]
# Geef een overzicht met daarin per land de naam van het land, de naam van de stad waar de verkoopafdeling is gevestigd (noem de kolomnaam in het overzicht ‘verkoper’) en het aantal steden waar zich klanten bevinden in dat land (noem de kolomnaam in het overzicht ‘klanten’) (3 kolommen, 29 rijen) 

# %%
table_data = get_table_data(['retailer_site', 'country'])

grouped_data = table_data.groupby('COUNTRY').agg(
    verkoper=('CITY', 'first'),
    klanten=('CITY', 'nunique')
).reset_index()

pandas.DataFrame(grouped_data)


# %% [markdown]
# ## Pythonvertalingen van SUBSELECT en UNION met o.a. for-loops

# %% [markdown]
# Geef een overzicht met daarin de voornaam en de achternaam van de medewerkers die nog nooit wat hebben verkocht (2 kolommen, 25 rijen) 

# %%
sales_staff_data = get_table_data('sales_staff')
order_header_data = get_table_data('order_header')

merged_data = sales_staff_data.merge(order_header_data, on='SALES_STAFF_CODE', how='left')
filter = merged_data[merged_data['ORDER_NUMBER'].isna()]

filter[['FIRST_NAME', 'LAST_NAME']]

# %% [markdown]
# Geef een overzicht met daarin het aantal producten waarvan de marge lager is dan de gemiddelde marge van alle producten samen. Geef in het overzicht tevens aan wat de gemiddelde marge is van dit aantal producten waarvan de marge lager dan de gemiddelde marge van alle producten samen is. (1 kolom, 2 rijen) 

# %%
product_data = get_table_data('product')

gem_marge = product_data['MARGIN'].mean()
filter = product_data['MARGIN'] < gem_marge

print(filter.sum())

# %% [markdown]
# Geef een overzicht met daarin de namen van de producten die voor meer dan 500 (verkoopprijs) zijn verkocht maar nooit zijn teruggebracht. (1 kolom, 13 rijen) 

# %%
product_data = get_table_data('product')
order_details_data = get_table_data('order_details')
return_item_data = get_table_data('returned_item')

merged_data = product_data.merge(order_details_data, on='PRODUCT_NUMBER', how='left')
merged_data2 = merged_data.merge(return_item_data, on='ORDER_DETAIL_CODE', how='left')
filter = merged_data2.loc[(merged_data2['RETURN_REASON_CODE'].notna()) & (merged_data2['UNIT_PRICE'] > 500)]
filter = filter[['PRODUCT_NAME']].drop_duplicates()

pandas.DataFrame(filter['PRODUCT_NAME'])

# %% [markdown]
# Geef een overzicht met daarin per (achternaam van) medewerker of hij/zij manager is of niet, door deze informatie toe te voegen als extra 'Ja/Nee'-kolom.<br>
# Hint: gebruik een for-loop waarin je o.a. bepaalt of het woord 'Manager' in de functie (position_en) staat. (2 kolommen, 102 rijen).

# %%
sales_staff_data = get_table_data('sales_staff')

is_manager = []

for position in sales_staff_data['POSITION_EN']:
    if 'Manager' in str(position):
        is_manager.append('Ja')
    else:
        is_manager.append('Nee')

sales_staff_data['IS_MANAGER'] = is_manager
overview = sales_staff_data[['LAST_NAME', 'IS_MANAGER']]

pandas.DataFrame(overview)

# %% [markdown]
# Met de onderstaande code laat je Python het huidige jaar uitrekenen.

# %%
from datetime import date
date.today().year

# %% [markdown]
# Met de onderstaande code selecteer je op een bepaald jaartal uit een datum.

# %%
from datetime import datetime

date_str = '16-8-2013'
date_format = '%d-%m-%Y'
date_obj = datetime.strptime(date_str, date_format)

date_obj.year

# %% [markdown]
# Geef met behulp van bovenstaande hulpcode een overzicht met daarin op basis van het aantal jaar dat iemand in dienst is of een medewerker ‘kort in dienst’ (minder dan 25 jaar in dienst) of een ‘lang in dienst’ (groter gelijk dan 12 jaar in dienst) is. Geef daarbij per medewerker in een aparte kolom zowel ‘kort in dienst’ als ‘lang in dienst’ aan. Gebruik (wederom) een for-loop.<br>
# (2 kolommen, 102 rijen) 

# %%
from datetime import date, datetime 

sales_staff_data = get_table_data('sales_staff')

in_dienst = []

current_year = date.today().year
date_format = '%Y-%m-%d'

for hire_date in sales_staff_data['DATE_HIRED']: 
    hire_year = datetime.strptime(hire_date, date_format).year
    if (current_year - hire_year) < 25:
        in_dienst.append('kort in dienst')
    else:
        in_dienst.append('lang in dienst')

sales_staff_data['DIENST_TIJD'] = in_dienst
overview = sales_staff_data[['LAST_NAME', 'DIENST_TIJD']]

pandas.DataFrame(overview)

# %% [markdown]
# ## Van Jupyter Notebook naar Pythonproject

# %% [markdown]
# 1. Richt de map waarin jullie tot nu toe hebben gewerkt in volgens de mappenstructuur uit de slides.
# 2. Maak van de ontstane mappenstructuur een Pythonproject dat uitvoerbaar is vanuit de terminal. Maak daarin een .py-bestand dat minstens 5 antwoorden uit dit notebook (in de vorm van een DataFrame) exporteert naar Excelbestanden. Alle notebooks mogen als notebook blijven bestaan.
# 3. Zorg ervoor dat dit Pythonproject zijn eigen repo heeft op Github. Let op: je virtual environment moet <b><u>niet</u></b> meegaan naar Github.
# 
# Je mag tijdens dit proces je uit stap 1 ontstane mappenstructuur aanpassen, zolang je bij het beoordelingsmoment kan verantwoorden wat de motivatie hierachter is. De slides verplichten je dus nergens toe.


