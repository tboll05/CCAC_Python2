# This program prompts the user for input (a type of activity they are interested in)
# Using this input, the program connects with the Bored API and produces a list of 3 suggested activities the user could do.

import requests, json

def get_activity_type():
    print("You look bored.  What kind of activity would you like to do?")
    print("Choose from the following types of activities:")
    print("Education, Recreational, Social, DIY, Charity, Cooking, Relaxation, Music, Busywork")
    activity_type = input("What will it be?").lower()
    return activity_type

def create_url(activity_type):
    API_ENDPOINT = "http://www.boredapi.com/api/"
    ending = "activity?type=%s" % (activity_type)
    full_url = API_ENDPOINT + ending
    return full_url

def produce_activity_list_of_3(full_url):
    print()
    print("Here are some suggestions for things you could do.")
    
    number = 1
    
    for item in range(3):
        response = requests.get(full_url)
        payload_objects = json.loads(response.text)
        print(number,".", payload_objects['activity'])
        number += 1

def main():
    myType = get_activity_type()
    full_url = create_url(myType)
    produce_activity_list_of_3(full_url)



main()