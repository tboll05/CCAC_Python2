import csv

#Function to build dictionary using csv file as parameter.
def buildDictionary(f):
    
    summaryDict = {'Facility Amount': {}, 'Chemical': {}, 'City': {}, 'Average Release Amount': 0.0, 'Total Records': 0}

    with open(f) as file:
        fileReader = csv.DictReader(file)

        for record in fileReader:
            
            #Keep track of how many records are in the file
            summaryDict['Total Records'] += 1

            #Add up all the estimated release amounts
            summaryDict['Average Release Amount'] += float(record['REL_EST_AMT'])

            if record['FACILITY_NAME'] not in summaryDict['Facility Amount']:
                #we need to add the facility name to our dict, with count 1
                summaryDict['Facility Amount'][record['FACILITY_NAME']] = float(record['REL_EST_AMT'])
            else:
                #when already in, increment by 1
                summaryDict['Facility Amount'][record['FACILITY_NAME']] += float(record['REL_EST_AMT'])

            if record['CHEM_NAME'] not in summaryDict['Chemical']:
                #we need to add the chemical name to our dict, with count 1
                summaryDict['Chemical'][record['CHEM_NAME']] = 1
            else:
                #when already in, increment by 1
                summaryDict['Chemical'][record['CHEM_NAME']] += 1

            if record['CITY_NAME'] not in summaryDict['City']:
                #we need to add the city name to our dict, with count 1
                summaryDict['City'][record['CITY_NAME']] = 1
            else:
                #when already in, increment by 1
                summaryDict['City'][record['CITY_NAME']] += 1

        #Calculate the average esitmated release amount across all facilities
        summaryDict['Average Release Amount'] = round(summaryDict['Average Release Amount'] / summaryDict['Total Records'], 2)
        
        #Return the final summary dictionary
        return summaryDict
    
#Function for filtering the top companies with the most estimated release amounts
def top_N_estimated_facility_release(userDict, n):
    count = 0
    
    #Loop that will put the company names in opder based on total estimated release amount in descending order
    for item in sorted(userDict['Facility Amount'].items(), key = lambda item: item[1], reverse = True):
        print(item[0] + ":", "{:,}".format(round(item[1],2)))
        count += 1
        if count >= n:
            break

            
#Actual Program Run            

myDict = buildDictionary('tri_air.csv')
            
topN = int(input("How many of the highest releasing facilities do you want to see?"))

top_N_estimated_facility_release(myDict, topN)