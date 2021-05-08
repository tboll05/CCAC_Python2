#Code written by Timothy Bollig
#Inquiry Question: How do weapons commonly used in aggravated assaults compare to those used in robberies?

##########################################
import requests, sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
##########################################

#####################################################################################################
#Function to check if the user is connected to the Internet.
#####################################################################################################  
def network_check():
    response = requests.get('http://google.com')
    return response.status_code

#####################################################################################################
#Function to check if the webpage returns a 200 status code.
##################################################################################################### 
def check_status_code(url):
    response = requests.get(url)
    return response.status_code

#####################################################################################################
#Take in the url of the data table and pass it to BeautifulSoup and return the parsed HTML code text.
#####################################################################################################  
def get_beautifulsoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

######################################################################################################
#Build a list of the header values.  These will be the keys for the dataframe we will build.
#Creates and returns a list of the header values.
######################################################################################################
def scrape_headers(soup):
    columns = soup.find_all(scope = 'col')
    headers = []
    for column in columns:
        headers.append(column.get_text().strip())
    return headers

######################################################################################################
#Get values from the first column, which uses a different id than the others.
#Creates and return a list of the first column values.
######################################################################################################
def first_column_values(soup):
    #These tables categorize the first column different from the others.  Uses headers ID.
    column_html = soup.find_all(headers = 'cell30')
    values = []
    for line in column_html:
        values.append(line.get_text().strip())
    return values

######################################################################################################
#Given a table column id, scrapes the values from the column and returns them in a list.
######################################################################################################
def scrape_values(soup, column_id):
    column_html = soup.find_all("td", class_ = lambda value: value and value.startswith(column_id))
    column_values = []
    for line in column_html:
        #This is initally a string in which some numbers contain commas.
        value = line.get_text().strip()
        #Replace any commas in the value with nothing so you can cast to an int.
        value = value.replace(',', '')
        #Cast to an int
        value = int(value)
        #Append to list
        column_values.append(value)
    return column_values
######################################################################################################
#Takes in the header values and lists of values for each column.
#Builds and returns a dataframe representation of the table.
######################################################################################################
def build_dataframe(headers, col1, col2, col3, col4, col5, col6, col7, col8):
    data = {
        headers[0] : col1,
        headers[1] : col2,
        headers[2] : col3,
        headers[3] : col4,
        headers[4] : col5,
        headers[5] : col6,
        headers[6] : col7,
        headers[7] : col8,
    }
    df = pd.DataFrame(data)
    return df

######################################################################################################
#Creates and returns a databace connection object and cursor object to fbi_stats.db.
#If this database doesn't exist then sqlite creates it within the same directory.
######################################################################################################
def connect_to_database():
    try:
        dbconn = sqlite3.connect('fbi_stats.db')
        cursor = dbconn.cursor()
        print()
        print("Successfully Connected to SQLite Database")
    except sqlite3.Error as error:  
        print("Error while connecting to SQLite", error)
        dbconn = handle_DB_Error(dbconn, cursor)
    return dbconn, cursor

######################################################################################################
#Handles sqlite3 errors by rolling back transactions and closing DB resources.
######################################################################################################
def handle_DB_Error(dbconn, cursor):
    if dbconn:
        try:
            #rollback changes since the last commit
            dbconn.rollback()
            print('Rolled back transaction.')
        
        except sqlite3.Error as error:
            print('Error rolling back transaction.', error)
            
        finally:
            #call function to close DB connection and cursor
            close_DB_Resources(dbconn, cursor)
            dbconn = None
            return dbconn

######################################################################################################
#Close the DB Connection and Cursor so the DB won't become locked.
######################################################################################################
def close_DB_Resources(dbconn, cursor):
    try:
        cursor.close()
        dbconn.close()
        print()
        print('DB resources were closed successfully.')
    
    except sqlite3.Error as error:
        print('Error occurred closing DB resources.', error)
    
 
######################################################################################################
#Create a table in the database called "robbery_weapon_stats".
######################################################################################################
def create_robbery_table_sql(dbconn, cursor):
    #Drop table if it already exists.
    drop_existing_table = '''
        DROP TABLE IF EXISTS robbery_weapon_stats;
    '''
    
    #Create table statement written in SQL.
    create_robbery_weapon_table_sql = '''
        CREATE TABLE IF NOT EXISTS
            robbery_weapon_stats(
            id INTEGER PRIMARY KEY,
            state TEXT NOT NULL,
            total_robberies INTEGER,
            firearms INT,
            knives_cutting_weapons INT,
            other_weapons INT,
            strong_arm INT,
            agency_count INT,
            population INT
        )
    '''
    try:
        #Execute above SQL code.
        cursor.execute(drop_existing_table)
        #Commit the changes to the database made by the SQL statement executed.
        dbconn.commit()
        #Using the database connection established by the connect_to_database function, execute the SQL code provided above against that database.
        cursor.execute(create_robbery_weapon_table_sql)
        #Commit the changes to the database made by the SQL statement executed.
        dbconn.commit()
        print()
        print('Table created or accessed successfully.')
        
    except sqlite3.Error as error:
        print('Error occurred when creating table.', error)
        dbconn = handle_DB_Error(dbconn, cursor)
    
    #Will be None if error occurred.
    return dbconn

######################################################################################################
#Create a table in the database called "assault_weapon_stats".
######################################################################################################
def create_assault_table_sql(dbconn, cursor):
    #Drop the table if it already exists
    drop_existing_table = '''
        DROP TABLE IF EXISTS assault_weapon_stats;
    '''
    
    #Create table statement written in SQL.
    create_assault_weapon_table_sql = '''
        CREATE TABLE IF NOT EXISTS
            assault_weapon_stats(
            id INTEGER PRIMARY KEY,
            state TEXT NOT NULL,
            total_assaults INTEGER,
            firearms INT,
            knives_cutting_weapons INT,
            other_weapons INT,
            personal_weapons INT,
            agency_count INT,
            population INT
        )
    '''
    try:
        #Execute above SQL code.
        cursor.execute(drop_existing_table)
        #Commit the changes to the database made by the SQL statement executed.
        dbconn.commit()
        #Using the database connection established by the connect_to_database function, execute the SQL code provided above against that database.
        cursor.execute(create_assault_weapon_table_sql)
        #Commit the changes to the database made by the SQL statement executed.
        dbconn.commit()
        print()
        print('Table created or accessed successfully.')
        
    except sqlite3.Error as error:
        print('Error occurred when creating table.', error)
        dbconn = handle_DB_Error(dbconn, cursor)
    
    #Will be None if error occurred.
    return dbconn

######################################################################################################
#Change the headers in a dataframe to match those of a given SQL table.
######################################################################################################
def change_dataframe_column_names(cursor,sql_table,dataframe):
    data = cursor.execute(f'PRAGMA table_info({sql_table})')
    
    #To be filled list of new column names
    new_columns = []
    
    for d in data:
        new_columns.append(d[1])
    
    #Remove the first item since this will be the ID column that is automatically created by SQL.
    new_columns.pop(0)
    
    #Set the columns of the dataframe to the list of column names from the SQL table
    dataframe.columns = new_columns

######################################################################################################
#Insert data from a dataframe into a SQL database table.
######################################################################################################
def insert_dataframe_to_sqlite_DB(dataframe, sql_table, dbconn):
    dataframe.to_sql(sql_table, dbconn, if_exists='replace', index=False)
    dbconn.commit()

######################################################################################################
#Query the robbery weapon stats SQL table and get totals for each type of weapon.
#Returns these totals in a list ordered as: firearms total, knives totals, other weapons, strong arm totals.
######################################################################################################
def get_robbery_totals(cursor):
    get_firearm_totals = '''
    SELECT SUM(firearms) FROM robbery_weapon_stats;
    '''
    get_knives_totals = '''
        SELECT SUM(knives_cutting_weapons) FROM robbery_weapon_stats;
    '''
    get_other_weapon_totals = '''
        SELECT SUM(other_weapons) FROM robbery_weapon_stats;
    '''
    get_strong_arm_totals = '''
        SELECT SUM(strong_arm) FROM robbery_weapon_stats;
    '''

    list_of_queries = [get_firearm_totals, get_knives_totals, get_other_weapon_totals, get_strong_arm_totals]

    totals = []

    for query in list_of_queries:
        cursor.execute(query)
        records = cursor.fetchall()
        value = records[0][0]
        totals.append(value)
        
    return totals

######################################################################################################
#Query the assault weapon stats SQL table and get totals for each type of weapon.
#Returns these totals in a list ordered as: firearms total, knives totals, other weapons, personal weapon totals.
######################################################################################################
def get_assault_totals(cursor):
    get_firearm_totals = '''
    SELECT SUM(firearms) FROM assault_weapon_stats;
    '''
    get_knives_totals = '''
        SELECT SUM(knives_cutting_weapons) FROM assault_weapon_stats;
    '''
    get_other_weapon_totals = '''
        SELECT SUM(other_weapons) FROM assault_weapon_stats;
    '''
    get_personal_weapon_totals = '''
        SELECT SUM(personal_weapons) FROM assault_weapon_stats;
    '''

    list_of_queries = [get_firearm_totals, get_knives_totals, get_other_weapon_totals, get_personal_weapon_totals]

    totals = []

    for query in list_of_queries:
        cursor.execute(query)
        records = cursor.fetchall()
        value = records[0][0]
        totals.append(value)
        
    return totals

######################################################################################################
#Query the assault weapon stats SQL table and get top 10 states by total number of assaults.
######################################################################################################
def get_assault_top_10_states(dbconn):
    df = pd.read_sql_query("SELECT state AS State, total_assaults AS [Total Assaults] FROM assault_weapon_stats ORDER BY total_assaults DESC LIMIT 10", dbconn)
    return df

######################################################################################################
#Query the robbery weapon stats SQL table and get top 10 states by total number of robberies.
######################################################################################################
def get_robberies_top_10_states(dbconn):
    df = pd.read_sql_query("SELECT state AS State, total_robberies AS [Total Robberies] FROM robbery_weapon_stats ORDER BY total_robberies DESC LIMIT 10", dbconn)
    return df


######################################################################################################
#Main Program
######################################################################################################
def main():
    #Check to ensure the device is connected to the Internet. If you get a status_code of any kind, you have an internet connection.
    #If Internet connection found, set program switch to True (On).
    try:
        network_check()
        switch = True
    #If no internet connection found you will get an error and the program will print a warning message and set switch to False (Off)
    except:
        print('No Internet Connection Found')
        switch = False

    #Switch being true means you are connected to the Internet.
    if switch == True:
        
        #Check if both webpages are returned with a 200 status code.
        url1 = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-22'
        status1 = check_status_code(url1)
        url2 = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-21'
        status2 = check_status_code(url2)

        #If both webpages have a 200 status code, run rest of the program
        if status1 == 200 and status2 == 200:

            #Scraping and Building the Assaults Dataframe.
            #Web address for FBI Aggravated Assaults by Weapon Type 2019 Table.
            url = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-22'
            #Obtain webpage HTML code.
            soup = get_beautifulsoup(url)
            #Scrape table data.
            headers = scrape_headers(soup)
            states = first_column_values(soup)
            agg_assaults = scrape_values(soup,"odd group1")
            firearms = scrape_values(soup,"even group2")
            knives = scrape_values(soup,"odd group3")
            other_weapons = scrape_values(soup,"even group4")
            personal_weapons = scrape_values(soup,"odd group5")
            agency_count = scrape_values(soup,"even group6")
            populations = scrape_values(soup,"odd group7")
            #Produce dataframe with scraped data.
            assaults_dataframe = build_dataframe(headers, states, agg_assaults, firearms, knives, other_weapons, personal_weapons, agency_count, populations)

            #Scraping and Building the Robbery Dataframe
            #Web address for FBI Robbery by Weapon Type 2019 Table.
            url = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-21'
            #Obtain webpage HTML code.
            soup = get_beautifulsoup(url)
            #Scrape table data.
            headers = scrape_headers(soup)
            states = first_column_values(soup)
            robberies = scrape_values(soup,"odd group1")
            firearms = scrape_values(soup,"even group2")
            knives = scrape_values(soup,"odd group3")
            other_weapons = scrape_values(soup,"even group4")
            strong_arm = scrape_values(soup,"odd group5")
            agency_count = scrape_values(soup,"even group6")
            populations = scrape_values(soup,"odd group7")
            #Produced dataframe with scraped data.
            robberies_dataframe = build_dataframe(headers, states, robberies, firearms, knives, other_weapons, strong_arm, agency_count, populations)

            #Connect to database/create one if not already existing.
            dbconn, cursor = connect_to_database()

            #Create tables in SQL to store scraped data.
            create_assault_table_sql(dbconn, cursor)
            create_robbery_table_sql(dbconn, cursor)

            #Change the column headers of the dataframes to match those of the target SQL tables.
            #This will make data insertion smoother.
            change_dataframe_column_names(cursor,'assault_weapon_stats', assaults_dataframe)
            change_dataframe_column_names(cursor,'robbery_weapon_stats', robberies_dataframe)

            #Insert dataframes into the respective database tables.
            insert_dataframe_to_sqlite_DB(assaults_dataframe, 'assault_weapon_stats', dbconn)
            insert_dataframe_to_sqlite_DB(robberies_dataframe, 'robbery_weapon_stats', dbconn)

            #Create unpivoted dataframes in order to visualize as a barplot with Seaborn.
            #unpivot_assault_df = assaults_dataframe.melt(id_vars = ['state'], value_vars = ['firearms', 'knives_cutting_weapons', 'other_weapons', 'personal_weapons'], var_name = 'Weapon Type', value_name = 'Count')
            #unpivot_robbery_df = robberies_dataframe.melt(id_vars = ['state'], value_vars = ['firearms', 'knives_cutting_weapons', 'other_weapons', 'strong_arm'], var_name = 'Weapon Type', value_name = 'Count')

            #Query the SQL tables to build lists of SUMs for the different weapon types.
            total1 = get_assault_totals(cursor)
            total2= get_robbery_totals(cursor)
            #Create dataframes using these sums to be visualized as column charts.
            df1 = pd.DataFrame({'Weapon Used in Assault':['Firearms', 'Knives and Cutting', 'Other', 'Personal'], 'Totals':total1})
            df2 = pd.DataFrame({'Weapon Used in Robbery':['Firearms', 'Knives and Cutting', 'Other', 'Strong Arm'], 'Totals':total2})

            #Build dataframes for top 10 states in total assaults and robberies.
            top_assault_states = get_assault_top_10_states(dbconn)
            top_robbery_states = get_robberies_top_10_states(dbconn)

            ###############################################
            #Code for displaying visuals.
            ###############################################
            #Create column charts for each table.
            figure, axes = plt.subplots(nrows=1, ncols=2, figsize=(18,5))
            figure.suptitle("Comparison of Weapons Used in Assaults vs Robberies")
            df1.plot.bar(x='Weapon Used in Assault', rot= 0, ax=axes[0])
            df2.plot.bar(x='Weapon Used in Robbery', rot= 0, ax=axes[1])
            plt.show()

            #Create barplot for each unpivoted dataframe using Seaborn.
            #figure = plt.figure(figsize=(18,5))
            #figure.add_subplot(1,2,1)
            #sb1 = sns.barplot(x='Weapon Type', y='Count', data=unpivot_assault_df)
            #figure.add_subplot(1,2,2)
            #sb2 = sns.barplot(x='Weapon Type', y='Count', data=unpivot_robbery_df)
            #sb1.set(xlabel='Weapons in Assaults')
            #sb2.set(xlabel='Weapons in Robberies')
            #sb2.set(ylabel=None)
            #plt.show()

            #Insert code for Top 10 state bar charts.
            figure = plt.figure(figsize=(18,5))
            figure.suptitle("Comparison of Top 10 States in Aggravated Assaults and Robberies")
            figure.add_subplot(1,2,1)
            sns.set_color_codes("pastel")
            sb1 = sns.barplot(x="Total Assaults", y="State", data=top_assault_states, color="b")
            figure.add_subplot(1,2,2)
            sns.set_color_codes("pastel")
            sb2 = sns.barplot(x="Total Robberies", y="State", data=top_robbery_states, color="b") 
            sb2.set(ylabel=None)
            plt.show()

            #Close the database connection and cursor
            close_DB_Resources(dbconn,cursor)
        
        #If at least one of the webpages has a status code other than 200, print out an error message and the program ends.
        else:
            if status1 != 200 and status2 != 200:
                print('Problem with both', url1, 'and', url2)
            elif status1 != 200:
                print('Problem with', url1)
            else:
                print('Problem with', url2)

    #If there is no Internet connection, print out error message and end the program.
    else:
        print('Please connect to the Internet and try again.')

main()