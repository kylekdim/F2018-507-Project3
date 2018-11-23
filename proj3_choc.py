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
        DROP TABLE IF EXISTS 'Teams';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Rounds';
    '''
    cur.execute(statement)
    conn.commit()
    
    # Create 'Teams' Table
    statement = '''
        CREATE TABLE 'Teams' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Seed' INTEGER NOT NULL,
            'Name' TEXT NOT NULL,
            'ConfRecord' TEXT NOT NULL
        );
    '''
    try:
        cur.execute(statement)
    except:
        print("Creation of Database Failed with 'Teams'. Please try again.")
    conn.commit()

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
