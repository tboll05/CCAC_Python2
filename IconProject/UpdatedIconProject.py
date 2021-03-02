#This program prompts the user to enter 100 integers of either 1 or 0 and then converts these into a picture in a 10x10 grid.
#1 represents a filled or on pixel and 0 represents a blank or off pixel.


#Prompt user to input 10 10 digit binary integers made up of 1s and 0s.  Each 10 digit intger is made into a list and then inserted into an overall list.
#The final result is a list of 10 lists, each containing 10 integers of 1 or 0.
def read():
    data = []
    count = 1

    for line in range(10):
        tempString = input(f"Please enter your 10 numbers for row {count}: ")
        data.append(list(tempString))
        count += 1

    return data

#Nested loop to change contents of data structure.  1s become asterisks and 0s become empty strings.
def convert(data):
    for line in data:
        index = 0
        for item in line:
            if item == '0':
                line[index] = ' '
            else:
                line[index] = '*'
            index += 1

#Function to accept an integer to scale image by
def scale():
    return int(input("Scale? (Any whole number greater than 0): "))

#Print out picture in a 10 x 10 grid
def display(data, scale):
    for line in data:
        for item in line:
            print(item * scale, end = " ")
        print()
        if scale > 1:
            numLines = 1
            while numLines != scale:
                for item in line:
                    print(item * scale, end = " ")
                print()
                numLines += 1


#Invert data so the picture will be upside down.
def invert(data):
    invertedData = []

    for line in reversed(data):
        invertedData.append(line)

    return invertedData



#Actual program run

#Print statements
print('Hello, welcome to Icon Processing.')
print()
print('Please have your icon ready.  You will be asked to enter your 100 1s and 0s in groups of 10.')
print('\t"1s" will be interpreted as a filled pixel.')
print('\t"0s" will be interpreted as a blank pixel.')
input("Press ENTER when you are ready to continue.")
print()
print('Remember: This program requires you enter your numbers without any spaces, tabs, or commas')


#Functions
data = read()
convert(data)

scale = scale()

inverted = input("Invert? (Y/N): ")

if inverted.upper() == 'Y':
    invertedData = invert(data)
    display(invertedData, scale)
else:
    display(data, scale)