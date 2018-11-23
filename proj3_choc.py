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
    print("error msg")

#drop tables like hw10

cur.execute(statement)
conn.commit()

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

#=========================================


    # Create 'Games' Table
    statement = '''
        CREATE TABLE 'Games' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Winner' INTEGER NOT NULL,
            'Loser' INTEGER NOT NULL,
            'WinnerScore' INTEGER NOT NULL,
            'LoserScore' INTEGER NOT NULL,
            'Round' INTEGER NOT NULL,
            'Time' TEXT NOT NULL
        );
    '''
    try:
        cur.execute(statement)
    except:
        print("Creation of Database Failed with 'Games'. Please try again.")
    conn.commit()

    # Create 'Rounds' Table
    statement = '''
        CREATE TABLE 'Rounds' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Date' TEXT  NOT NULL
        );
    '''
    try:
        cur.execute(statement)
    except:
        print("Creation of Database Failed with 'Rounds'. Please try again.")
    conn.commit()
    conn.close()

def populate_tournament_db():

    # Connect to big10 database
    conn = sqlite.connect('changkyle_big10.sqlite')
    cur = conn.cursor()

    

    # Your code goes here
    # HINTS:
    # Column order in teams.csv file: Seed,Name,ConfRecord
    # Column order in games.csv file: Winner,Loser,WinnerScore,LoserScore,Round,Time
    # Column order in rounds.csv file: Name,Date
    
    # read data from Teams.csv
    with open("teams.csv", 'r') as csv_file_t:
        csv_teams = csv.reader(csv_file_t)

        for row in csv_teams:
            (Seed, Name, ConfRecord) = row

            insert_statement = '''
                INSERT INTO Teams(Seed, Name, ConfRecord) VALUES (?, ?, ?);
            '''
            # execute + commit
            cur.execute(insert_statement, [Seed, Name, ConfRecord])
            conn.commit()


    # read data from Games.csv
    with open("games.csv", 'r') as csv_file_g:
        csv_games = csv.reader(csv_file_g)

        for row in csv_games:
            (Winner, Loser, WinnerScore, LoserScore, Round, Time) = row

            insert_statement = '''
                INSERT INTO Games(Winner, Loser, WinnerScore, LoserScore, Round, Time) VALUES (?, ?, ?, ?, ?, ?);
            '''
            # execute + commit
            cur.execute(insert_statement, [Winner, Loser, WinnerScore, LoserScore, Round, Time])
            conn.commit()

    # read data from Rounds.csv
    with open("rounds.csv", 'r') as csv_file_r:
        csv_rounds = csv.reader(csv_file_r)

        for row in csv_rounds:
            (Name, Date) = row

            insert_statement = '''
                INSERT INTO Rounds(Name, Date) VALUES (?, ?);
            '''
            # execute + commit
            cur.execute(insert_statement, [Name, Date])
            conn.commit()

    # Close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tournament_db()
    print("Created big10 Database")
    populate_tournament_db()
    print("Populated big10 Database")


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
