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
    
    with open("teams.csv", 'r') as csv_file_t:  
    
    with open("flavors_of_cacao_cleaned.csv", 'r') as csv_file_c:
        csv_data = csv.reader(csv_file_c)

        for row in csv_data:
            (Company, SpecificBeanBarName, REF, ReviewDate, CocoaPercent, CompanyLocation, Rating, BeanType, BroadBeanOrigin) = row

            CocoaPercent = float(CocoaPercent.strip('%'))

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


# Part 2: Implement logic to process user commands
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
