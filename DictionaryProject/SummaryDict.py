import csv

#Function to build dictionary using csv file as parameter.
def buildDictionary(f):
    
    #Initialize summary dictionary.
    summaryDict = {'Facility Amount': {}, 'Chemical': {}, 'City': {}, 'Average Release Amount': 0.0, 'Total Records': 0}

    #Open file and pass it to DictReader.
    with open(f) as file:
        fileReader = csv.DictReader(file)


        #Iterate through each row in the data file.
        for record in fileReader:
            
            #Keep track of how many records are in the file.
            summaryDict['Total Records'] += 1

            #Add up all the estimated release amounts.
            summaryDict['Average Release Amount'] += float(record['REL_EST_AMT'])

            #Check if the facility is an existing key in the summary dictionary.
            if record['FACILITY_NAME'] not in summaryDict['Facility Amount']:
                #If not existing, we need to add the facility name to our dictionary along with the release amount for this row.
                summaryDict['Facility Amount'][record['FACILITY_NAME']] = float(record['REL_EST_AMT'])
            else:
                #when already existing, we need to add this current row's release amount to the running total release amount for this facility.
                summaryDict['Facility Amount'][record['FACILITY_NAME']] += float(record['REL_EST_AMT'])

            #Check if the Chemical name exists in the summary dictionary.
            if record['CHEM_NAME'] not in summaryDict['Chemical']:
                #If not existing, we need to add the chemical name to our dict, with count 1.
                summaryDict['Chemical'][record['CHEM_NAME']] = 1
            else:
                #When already existing, increment by 1.
                summaryDict['Chemical'][record['CHEM_NAME']] += 1

            #Check if City Name exists in the summary dictionary.
            if record['CITY_NAME'] not in summaryDict['City']:
                #If not existing, we need to add the city name to our dictionary, with count 1.
                summaryDict['City'][record['CITY_NAME']] = 1
            else:
                #when existing, increment by 1.
                summaryDict['City'][record['CITY_NAME']] += 1


        #Calculate the average estimated release amount across all facilities.
        summaryDict['Average Release Amount'] = round(summaryDict['Average Release Amount'] / summaryDict['Total Records'], 2)
        
        #Return the final summary dictionary
        return summaryDict
    
#Function for filtering the top companies with the most estimated release amounts
def top_N_estimated_facility_release(userDict, n):
    count = 0
    
    #Loop that will put the company names in order based on total estimated release amount in descending order
    for item in sorted(userDict['Facility Amount'].items(), key = lambda item: item[1], reverse = True):
        print(item[0] + ":", "{:,}".format(round(item[1],2)))
        count += 1
        if count >= n:
            break

            


#Actual Program Run            

#Create a summary dictionary from a CSV file.
myDict = buildDictionary('tri_air.csv')


#Validate Input to be a whole number greater than 0.            
while True:
    
    #Ask user for input of whole number greater than 0.
    try:
        topN = int(input("How many of the highest releasing facilities do you want to see?" + " "))
        
        #Check if input is a negative number.
        if topN < 0:
            print("Please enter a whole number greater than 0.")

    #check if input is a string or float.
    except ValueError:
        print("Please enter a whole number greater than 0.")
        continue
    
    #If input is whole number greater than 0, break out of while loop.
    else:
        if topN > 0:
            break

#Print out the Average Release Amount across all facilities and then the Top N Releasing facilities where N is provided by the user.
print()
print("Average Release Amount across all facilities:", myDict['Average Release Amount'])
print()
print(f'Top {topN} facilities by release amount:')
print("-----------------------------------------")
top_N_estimated_facility_release(myDict, topN)