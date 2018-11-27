import sqlite3
import csv
import json

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
#------- Load CSV data -----------
#================================= 
    
with open(BARSCSV, 'r') as csv_file_b:
    csv_data = csv.reader(csv_file_b)

    next(csv_data) #added this command to skip first line of headers in CSV file

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

        # execute + commit
        cur.execute(insert_statement, [Company, SpecificBeanBarName, REF, ReviewDate, CocoaPercent, CompanyLocation, Rating, BeanType, BroadBeanOrigin])
        conn.commit()

    # close connection
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
def bars_query(specification="", keyword="", criteria="ratings", sort="top", limit="10"):

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    if "c1" in specification:
        statement = "SELECT SpecificBeanBarName, Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin "
        statement += "FROM Bars "
        statement += "JOIN Countries AS c1 ON Bars.CompanyLocationId = c1.Id "
    elif "c2" in specification:
        statement = "SELECT SpecificBeanBarName, Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin "
        statement += "FROM Bars "
        statement += "JOIN Countries AS c2 ON Bars.BroadBeanOriginId = c2.Id "
    else:
        statement = "SELECT SpecificBeanBarName, Company, CompanyLocation, Rating, CocoaPercent, BroadBeanOrigin "
        statement += "FROM Bars "

    # specification
    if specification != "":
        if "Alpha2" in specification:
            keyword = keyword.upper()
        try:
            statement += "WHERE {} = '{}' ".format(specification , keyword)
        except:
            print("Failure. Please try again.")

    # ORDER BY ratings / cocoa
    if criteria == "ratings":
        statement += "ORDER BY Rating "
    elif criteria == "cocoa":
        statement += "ORDER BY CocoaPercent "

    # ORDER BY top DESC / bottom ASC
    if sort == "top":
        statement += "DESC "
    elif sort == "bottom":
        statement += "ASC "

    # limit
    statement += "LIMIT {}".format(limit) #list the top <limit> matches or the bottom <limit> matches.

    # excute the statement
    # print(statement)
    results = []
    rows = cur.execute(statement).fetchall()
    for row in rows:
        results.append(row)
    conn.commit()

    return results

def companies_query(specification="", keyword="", criteria="ratings", sort="top", limit="10"):

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    
    if criteria == "ratings":
        statement = "SELECT Company, CompanyLocation, AVG(Rating) "
    elif criteria == "cocoa":
        statement = "SELECT Company, CompanyLocation, AVG(CocoaPercent) "
    elif criteria == "bars_sold":
        statement = "SELECT Company, CompanyLocation, COUNT(SpecificBeanBarName) "

    statement += "FROM Bars "

    if "c1.Alpha2" in specification:
        statement += "JOIN Countries AS c1 ON Bars.CompanyLocationId = c1.Id "
        statement += "GROUP BY Company "
        statement += "HAVING COUNT(SpecificBeanBarName) > 4 "
    elif "c2.Alpha2" in specification:
        statement += "JOIN Countries AS c2 ON Bars.BroadBeanOriginId = c2.Id "
        statement += "GROUP BY Company "
        statement += "HAVING COUNT(SpecificBeanBarName) > 4 "
    elif specification == "Alpha2" or specification == "Region":
        statement += "JOIN Countries ON Bars.CompanyLocation = Countries.EnglishName "
        statement += "GROUP BY Company "
        statement += "HAVING COUNT(SpecificBeanBarName) > 4 "
    else:
        statement += "GROUP BY Company "
        statement += "HAVING COUNT(SpecificBeanBarName) > 4 "

    if specification != "":
        if "Alpha2" in specification:
            keyword = keyword.upper()
        try:
            statement += "AND {} = '{}' ".format(specification , keyword)
        except:
            print("Failure. Please try again.")

    if criteria == "ratings":
        statement += "ORDER BY AVG(Rating) "
    elif criteria == "cocoa":
        statement += "ORDER BY AVG(CocoaPercent) "
    elif criteria == "bars_sold":
        statement += "ORDER BY COUNT(SpecificBeanBarName) "

    if sort == "top":
        statement += "DESC "
    elif sort == "bottom":
        statement += "ASC "

    statement += "LIMIT {}".format(limit)

    results = []
    rows = cur.execute(statement).fetchall()
    for row in rows:
        results.append(row)
    conn.commit()

    return results

def countries_query(specification="", keyword="", criteria="ratings", sort="top", limit="10", sellers_or_sources="sellers"):
    
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = "SELECT EnglishName, Region, "

    if criteria == "ratings":
        statement += "AVG(Rating) "
    elif criteria == "cocoa":
        statement += "AVG(CocoaPercent) "
    elif criteria == "bars_sold":
        statement += "COUNT(SpecificBeanBarName) "

    statement += "FROM Countries "

    if sellers_or_sources == "sellers":
        statement += "JOIN Bars ON Countries.Id = Bars.CompanyLocationId "
    elif sellers_or_sources == "sources":
        statement += "JOIN Bars ON Countries.Id = Bars.BroadBeanOriginId "

    statement += "GROUP BY EnglishName "
    statement += "HAVING COUNT(SpecificBeanBarName) > 4 "

    if specification != "":
        if "Region" in specification:
            keyword = keyword.title()
        try:
            statement += "AND {} = '{}' ".format(specification , keyword)
        except:
            print("Failure. Please try again.")

    if criteria == "ratings":
        statement += "ORDER BY AVG(Rating) "
    elif criteria == "cocoa":
        statement += "ORDER BY AVG(CocoaPercent) "
    elif criteria == "bars_sold":
        statement += "ORDER BY COUNT(SpecificBeanBarName) "

    if sort == "top":
        statement += "DESC "
    elif sort == "bottom":
        statement += "ASC "

    statement += "LIMIT {}".format(limit) 

    results = []
    rows = cur.execute(statement).fetchall()
    for row in rows:
        results.append(row)
    conn.commit()

    return results


def regions_query():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()


def process_command(command):
    command_list = command.split() #split command into a list of words
    #print(command_list)
    command_query = command_list[0] #split main query from rest of command
    #print(command_query)
    command_params = command_list[1:] #split parameters from command
    #print(command_params)

    valid_query = True

    #dictionary of possible valid params in query
    params_dic = {
        "specification":"",
        "keyword":"",
        "criteria":"ratings",
        "sort":"top",
        "limit":"10",
        "sellers_or_sources":"sellers"
    }

    if command_query in ["bars", "companies", "countries", "regions"]:

        #if command_params: #search the list of params after the first command query word

            for param in command_params: 

                #set the criteria parameter if present
                if param in ["cocoa", "ratings", "bars_sold"]:
                    params_dic["criteria"] = param

                # set the seller/sources parameter
                elif param in ["sellers", "sources"]:
                    params_dic["sellers_or_sources"] = param
        
                # look for parameters that use "=" assignment
                elif "=" in param:
                    param_equal_list = param.split("=")
            
                    #for each word in the parameter with "="
                    for word in param_equal_list:

                        # top/bottom & limit
                        if word in ["top", "bottom"]:
                            params_dic["sort"] = param_equal_list[0]
                            params_dic["limit"] = param_equal_list[1] 

                        # set geographic specs
                        elif word in ["sellcountry", "sourcecountry", "sellregion", "sourceregion", "country", "region", "sellers", "sources"]:
                            if param_equal_list[0] == "sellcountry":
                                params_dic["specification"] = "c1.Alpha2"
                            elif param_equal_list[0] == "sourcecountry":
                                params_dic["specification"] = "c2.Alpha2"
                            elif param_equal_list[0] == "sellregion":
                                params_dic["specification"] = "c1.Region"
                            elif param_equal_list[0] == "sourceregion":
                                params_dic["specification"] = "c2.Region"
                            elif param_equal_list[0] == "country":
                                params_dic["specification"] = "Alpha2"
                            else:
                                params_dic["specification"] = param_equal_list[0].title()

                        # set the second word after "=" to the keyword
                        params_dic["keyword"] = param_equal_list[1].title()
                else:
                    valid_query = False #if there were params, but encountered an invalid entry

    else:
        valid_query = False #if the first word was not one of the main commands

    if valid_query == False:
        print("Command not recognized: ", command, ". Please try again") #error message, 

    results=[]


    if command_query == "bars" and valid_query == True:
        #print(params_dic)
        results = bars_query(params_dic["specification"], params_dic["keyword"], params_dic["criteria"], params_dic["sort"], params_dic["limit"])
                
        print_spacing = "{0:15} {1:15} {2:15} {3:10} {4:10} {5:20}" #using format command below, define positions and spaces added to output

        for row in results:
            (specific_bean_bar_name, company, company_location, rating, cocoa_percent, broad_bean_origin) = row #create results tuple for bars
            
            #run the text through cleaning functions to properly format text
            print(print_spacing.format(clean_str_shorten(specific_bean_bar_name), clean_str_shorten(company), clean_str_shorten(company_location), clean_decimal_fix(rating), clean_percent_fix(cocoa_percent), clean_str_shorten(broad_bean_origin)))
        
        return results


    elif command_query == "companies" and valid_query == True:
        
        results = companies_query(params_dic["specification"], params_dic["keyword"], params_dic["criteria"], params_dic["sort"], params_dic["limit"])

        print_spacing = "{0:20} {1:20} {2:20}"
        for row in results:
            (company, company_location, agg) = row

            if params_dic["criteria"] == "ratings":
                agg = clean_decimal_fix(agg)
            elif params_dic["criteria"] == "cocoa":
                agg = clean_percent_fix(agg)

            print(print_spacing.format(clean_str_shorten(company), clean_str_shorten(company_location), agg))

        return results

    elif command_query == "countries" and valid_query == True:
        results = countries_query(params_dic["specification"], params_dic["keyword"], params_dic["criteria"], params_dic["sort"], params_dic["limit"], params_dic["sellers_or_sources"])

        print_spacing = "{0:20} {1:20} {2:20}"
        for row in results:
            (company, company_location, agg) = row

            if params_dic["criteria"] == "ratings":
                agg = clean_decimal_fix(agg)
            elif params_dic["criteria"] == "cocoa":
                agg = clean_decimal_fix(agg)

            print(template.format(str_output(company), str_output(region), agg))

        return results

    elif command_query == "regions" and valid_query == True:
        return regions_query(params_dic)

#=========================================
# ------ Results cleaning functions ------
#=========================================

def clean_str_shorten(string_output):
    if len(string_output) > 12:
        cleaned_output = string_output[:12] + "..." # shorten all words/phrases > 12 char in spec
    else:
        cleaned_output = string_output
    return cleaned_output
#=========================================

def clean_percent_fix(cocoa_content):
    cleaned_output = str(cocoa_content).replace(".0", "%") #replace decimal with percent
    return cleaned_output

#==========================================

def clean_decimal_fix(choc_rating):
    cleaned_output = "{0:.1f}".format(choc_rating, 1) #format rating to 1 decimal
    return cleaned_output

#========================================
#--------- Included Functions -----------
#========================================

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

        elif response == 'exit':
            print("Goodbye!")

        elif :
            "You have not entered a command. Please enter a valid command"
            continue
        
        else:
            #try:
            result = process_command(response)
            #print(result)
            #except:
                #print("Command not understood")
                #continue


# Make sure nothing runs or prints out when this file is run as a module

if __name__=="__main__":
    interactive_prompt()