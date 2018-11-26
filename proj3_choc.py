import sqlite3
import csv
import json

# want to test my commit here

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'

try:
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
except:
    print("Database creation failed at startup. Please try again.")

statement = '''
    DROP TABLE IF EXISTS 'Bars';
'''
cur.execute(statement)

statement = '''
    DROP TABLE IF EXISTS 'Countries';
'''
cur.execute(statement)
conn.commit()
    
# ==================================
# -------- Create Bars Table -------
# ==================================

statement = '''
    CREATE TABLE 'Bars' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Company' TEXT NOT NULL,
        'SpecificBeanBarName' TEXT NOT NULL,
        'REF' TEXT,
        'ReviewDate' TEXT,
        'CocoaPercent' REAL,
        'CompanyLocation' TEXT,
        'CompanyLocationId' INTEGER,
        'Rating' REAL,
        'BeanType' TEXT,
        'BroadBeanOrigin' TEXT,
        'BroadBeanOriginId' INTEGER
        );
    '''
try:
    cur.execute(statement)
except:
    print("Table creation failed at 'Bars'. Please try again.")
    
conn.commit()

# =======================================
# -------- Create Countries Table -------
# =======================================

statement = '''
        CREATE TABLE 'Countries' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' TEXT,
            'Alpha3' TEXT,
            'EnglishName' TEXT,
            'Region' TEXT,
            'Subregion' TEXT,
            'Population' INTEGER,
            'Area' REAL
        );
    '''
try:
    cur.execute(statement)
except:
    print("Table creation failed at 'Countries'. Please try again.")
conn.commit()

#=================================

# extra big 10 stuff for ref

#def populate_tournament_db():

    # Connect to big10 database
    #conn = sqlite.connect('changkyle_big10.sqlite')
    #cur = conn.cursor()
    
#with open("teams.csv", 'r') as csv_file_t:  
    
with open(BARSCSV, 'r') as csv_file_b:
    csv_data = csv.reader(csv_file_b)

    next(csv_data) #added this command to skip first line of headers in CSV file

    for row in csv_data:
        (Company, SpecificBeanBarName, REF, ReviewDate, CocoaPercent, CompanyLocation, Rating, BeanType, BroadBeanOrigin) = row

        #CocoaPercent = float(CocoaPercent.strip('%'))
        CocoaPercent = CocoaPercent.strip('%')
        CocoaPercent = float(CocoaPercent)

        try:
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()
        except:
            print("Failure. Please try again.")

        insert_statement = '''
            INSERT INTO Bars(Company, SpecificBeanBarName, REF, ReviewDate, CocoaPercent, CompanyLocation, Rating, BeanType, BroadBeanOrigin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        # execute and commit
        cur.execute(insert_statement, [Company, SpecificBeanBarName, REF, ReviewDate, CocoaPercent, CompanyLocation, Rating, BeanType, BroadBeanOrigin])
        conn.commit()
    # Close connection
    conn.commit()
    conn.close()


#===========================================
#------------ Load Json Data ---------------
#===========================================

json_file = open(COUNTRIESJSON, 'r')
json_content = json_file.read()
json_data = json.loads(json_content)

try:
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
except:
    print("Failure. Please try again.")

for row in json_data:
    Alpha2 = row["alpha2Code"]
    Alpha3 = row["alpha3Code"]
    EnglishName = row["name"]
    Region = row["region"]
    Subregion = row["subregion"]
    Population = row["population"]
    Area = row["area"]

    insert_statement = '''
        INSERT INTO Countries(Alpha2, Alpha3, EnglishName, Region, Subregion, Population, Area) VALUES (?, ?, ?, ?, ?, ?, ?);
    '''

    # execute + commit
    cur.execute(insert_statement, [Alpha2, Alpha3, EnglishName, Region, Subregion, Population, Area])
    conn.commit()


#====================================
#----- Update Tables----------------
#====================================

#sql for adding info to new columns

add_CompanyLocationId = '''
    UPDATE Bars
    SET (CompanyLocationId) = (SELECT c.ID FROM Countries c WHERE Bars.CompanyLocation = c.EnglishName)
'''

cur.execute(add_CompanyLocationId)

add_BroadBeanOriginId = '''
    UPDATE Bars
    SET (BroadBeanOriginId) = (SELECT c.ID FROM Countries c WHERE Bars.BroadBeanOrigin = c.EnglishName)
'''

cur.execute(add_BroadBeanOriginId)
conn.commit()

#Queries

# Part 2: Implement logic to process user commands
# To prepare for supporting interactive queries, in part 2 you will implement a function “process_command” that takes a command string and returns a list of tuples representing records that match the query.
# Your process_command function must be able to support four main commands, along with a variety of parameters for each. The four commands are ‘bars’, ‘companies’, ‘countries’, and ‘regions.’ Each command supports parameters and provides results as detailed below.


""" bars
Description: Lists chocolate bars, according the specified parameters.
Parameters:
sellcountry=<alpha2> | sourcecountry=<alpha2> | sellregion=<name> | sourceregion=<name> [default: none]
Description: Specifies a country or region within which to limit the results, and also specifies whether to limit by the seller (or manufacturer) or by the bean origin source.
ratings | cocoa [default: ratings]
Description: Specifies whether to sort by rating or cocoa percentage
top=<limit> | bottom=<limit> [default: top=10]
Description: Specifies whether to list the top <limit> matches or the bottom <limit> matches.
companies
Description: Lists chocolate bars sellers according to the specified parameters. Only companies that sell more than 4 kinds of bars are listed in results.
Parameters:
country=<alpha2> | region=<name> [default: none]
Description: Specifies a country or region within which to limit the results.
ratings | cocoa | bars_sold [default: ratings]
Description: Specifies whether to sort by rating, cocoa percentage, or the number of different types of bars sold
top=<limit> | bottom=<limit> [default: top=10]
Description: Specifies whether to list the top <limit> matches or the bottom <limit> matches.

countries
Description: Lists countries according to specified parameters. Only countries that sell/source more than 4 kinds of bars are listed in results.
Parameters:
region=<name> [default: none]
Description: Specifies a region within which to limit the results.
sellers | sources [default: sellers]
Description: Specifies whether to select countries based sellers or bean sources.
ratings | cocoa | bars_sold [default: ratings]
Description: Specifies whether to sort by rating, cocoa percentage, or the number of different types of bars sold
top=<limit> | bottom=<limit> [default: top=10]
Description: Specifies whether to list the top <limit> matches or the bottom <limit> matches.

regions
Description: Lists regions according to specified parameters. Only regions that sell/source more than 4 kinds of bars are listed in results.
Parameters:
sellers | sources [default: sellers]
Description: Specifies whether to select countries based sellers or bean sources.
ratings | cocoa | bars_sold [default: ratings]
Description: Specifies whether to sort by rating, cocoa percentage, or the number of different types of bars sold
top=<limit> | bottom=<limit> [default: top=10]
Description: Specifies whether to list the top <limit> matches or the bottom <limit> matches. 
"""
def bars_query():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

def companies_query():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

def countries_query():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

def regions_query():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

def process_command(command):
    return []


def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
