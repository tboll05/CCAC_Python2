#Timothy Bollig
#This program asks the user to input a type of activity and then queries the Bored API for activity suggestions that fall under that type of activity.
#It will build a list of 50 activities and then ask the user how many people they want to involve in the activity and filter the list down based on this criteria.
#Duplicate activities are removed and the final list is printed out for the user to see and pick from.


#Import modules used in the program
import requests, json, math


#Asks the user to select a type of activity they are interested in.  Returns this input.
def get_activity_type():
    print("You look bored.  What kind of activity would you like to do?")
    print("Choose from the following types of activities:")
    print("Education, Recreational, Social, DIY, Charity, Cooking, Relaxation, Music, Busywork")
    
    #Input validation for activity type.  Continues prompting user for input until a valid input is given.
    possible_input_values = ['education','recreational','social','diy','charity','cooking','relaxation','music','busywork']
    ask_for_input = True
    while ask_for_input == True:
        activity_type = input("What will it be?").lower()
        if activity_type in possible_input_values:
            ask_for_input = False
        else:
            print("That isn't a valid activity type.")
    
    return activity_type


#Using the activity type input by the user, this creates and returns a url address to be used when connecting to the API.
def create_url(activity_type):
    API_ENDPOINT = "http://www.boredapi.com/api/"
    ending = "activity?type=%s" % (activity_type)
    full_url = API_ENDPOINT + ending
    return full_url


#This will use the created url to query the API and build a bank of 50 activity suggestions.  It returns the 50 suggested activities in a list of dictionary objects.
def create_bank_of_activities(full_url):
    
    activity_bank = []
    print()
    print("Finding activities for you........")
    print()
    
    for item in range(50):
        #Querying the API for an activity suggestion of the given type.
        response = requests.get(full_url)
        #Transforming the response to a string object.
        payload_objects = json.loads(response.text)
        #Appending this result to a list that is the bank of activities suggested.
        activity_bank.append(payload_objects)
        
    return activity_bank


#This will ask the user for the number of friends in their group that they want to take part in the activities.  It will then take the bank of suggested activities
#and filter out the activities meant for less people than what the user has indicated.  It returns this remaining activities in a list of the activity names.
def filter_activities_by_participants(activity_bank):
    filtered_bank_of_activities = []
    
    #Force input to integer but truncating decimals.
    num_participants = math.trunc(float(input("How many people are in your group?")))
    
    #If the user wants to do something alone.  The program treats 0, 1, or any negative number as if the user wants to do something alone.
    if num_participants <= 1:
        for item in activity_bank:
            if item['participants'] == 1:
                filtered_bank_of_activities.append(item['activity'])
            else:
                pass
    
    #If the user wants to do something with at least one other person.
    else:
        for item in activity_bank:
            if item['participants'] >= num_participants:
                filtered_bank_of_activities.append(item['activity'])
            else:
                pass
    
    return filtered_bank_of_activities


#This will take the now filtered bank of activities and remove any duplicate suggestions.  The API returns activities at random so duplicates may exist in the original bank.
#This returns a list of unique activity suggestions of the provided type and for the provided number of participants.
def remove_duplicate_actvities(filtered_activity_bank):
    #List to hold unique activity suggestions.
    final_results = []
    
    for item in filtered_activity_bank:
        #Check if the activity is already listed in the final list.
        if item not in final_results:
            #If not, add it to the list.
            final_results.append(item)
            
    return final_results


#This will print out the final suggested activities in a numbered list.
def print_activities(final_results):
    number = 1
    print("Here are the activities we suggest for you.")
    print()
    for item in final_results:
        print(number, ".", item)
        number += 1
        

#Main program run.
def main():
    myType = get_activity_type()
    full_url = create_url(myType)
    activity_bank = create_bank_of_activities(full_url)
    activity_bank = filter_activities_by_participants(activity_bank)
    activity_bank = remove_duplicate_actvities(activity_bank)
    print_activities(activity_bank)


main()