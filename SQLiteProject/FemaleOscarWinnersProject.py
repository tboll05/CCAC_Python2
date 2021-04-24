#This program reads in a csv file of female oscar winners with their ages, year they won, and what movie they starred in.
#It then returns a list of rows for those winners who are 30 years of age or younger.

import csv, sqlite3

#Read in the contents of the csv file and organize it into a list of lists.
#Each item in the outer list represents a row in the csv file.
def read_file(csvfilename):
    #Opens csv file and read each line into a list called file_contents.
    with open(csvfilename, newline = '') as csvfile:
        osreader = csv.reader(csvfile)
        #List that will be returned by the function.  This will be a list made up of items that are also lists.
        file_contents = []
        #Look through the csv file and take each row and insert it into the file_contents list.
        for row in osreader:
            file_contents.append(row)
    #File_contents will be a list of lists.  Each item within this outer list represents a single row from the csv file.
    return file_contents

#Connect to the database and return the connection object.
def connect_to_database():
    #Connects to an existing database named female_oscar_ages.db.
    #If this database doesn't exist then sqlite creates it within the same directory that this script resides in.
    dbconn = sqlite3.connect('female_oscar_ages.db')
    return dbconn

#Create a table within the database to store the data from the csv file.
def create_table(dbconn):
    #Create table statement written in SQL.
    female_oscars_table = '''
        CREATE TABLE IF NOT EXISTS
            female_oscar_winners(
            id INTEGER PRIMARY KEY,
            year INTEGER NOT NULL,
            age INTEGER NOT NULL,
            name TEXT NOT NULL,
            movie TEXT NOT NULL
        )
    '''
    #Using the database connection established by the connect_to_database function, execute the SQL code provided above against that database.
    dbconn.cursor().execute(female_oscars_table)
    #Commit the changes to the database made by the SQL statement executed.
    dbconn.commit()

#Insert data from the csv file into the table created by the create_table function.    
def insert_data(file_contents, dbconn):
    #SQL statement to insert data from csv file.  The ?s mean that those input values will be based on an iterable. In this case, a list object from the file_contents list of lists.
    insert_statement = '''
        INSERT INTO female_oscar_winners (id, year, age, name, movie)
        VALUES (?,?,?,?,?)
    '''
    #For each list (row from the csv file) that comes in from the file_contents list of lists, do the following:
    for row in file_contents[1:]:
        #The first three values from the list have to be casted to integers to comply with the table data type constraints.
        row[0] = int(row[0])
        row[1] = int(row[1])
        row[2] = int(row[2])
        #Execute the SQL insert statement and use the values from the list (row) as the input values.
        dbconn.cursor().execute(insert_statement,row)
        #Commit the changes to the database.
        dbconn.commit()

#Using the connection to the database, return an ordered result set of female oscar winners 30 years of age or younger.     
def winners_under_30(dbconn):
    #SQL statement to return a filtered, ordered result set.
    winners_under_30 = '''
        SELECT * 
        FROM female_oscar_winners
        WHERE age <= 30
        ORDER BY age;
    '''
    
    #I am not sure why but I had to explicitly set the cursor to a variable for this to work.
    cursor = dbconn.cursor()
    #Execute the SQL query against the database.
    cursor.execute(winners_under_30)
    #Retrieve the result set returned by the SQL query.
    records = cursor.fetchall()
    #Results are returned as a list of tuples.
    return records

#Main program run.
def main():
    #Read file contents into a list of lists where each indexed item in the out list represents a single row from the csv file.
    file_contents = read_file('oscar_age_female.csv')
    #Connect to the database.
    dbconn = connect_to_database()
    #Create the table in the database if it doesn't already exist.
    create_table(dbconn)
    #Insert the data from file_contents into the newly created/already existing table.
    insert_data(file_contents,dbconn)
    #Obtain the result set of the 30 years of age or younger query.
    records = winners_under_30(dbconn)
    #print out the results of the query.
    for row in records:
        print(row)

main()