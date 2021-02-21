#This program reads in a data file of on (1) and off (0) values and prints them out into a picture.


#Read the csv file and pull data into a list of lists.  Becomes 1 list made up of 10 lists which each contain 10 elements.
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


#Print out picture in a 10 x 10 grid
def display(data):
    lineIndex = 0    
    elementIndex = 0    

    for line in data:
        for item in line:
            print(data[lineIndex][elementIndex], end = ' ')
            elementIndex += 1
        print()
        lineIndex += 1
        elementIndex = 0


#Invert data so the picture will be upside down.
def invert(data):
    invertedData = []

    for line in reversed(data):
        invertedData.append(line)

    return invertedData


#Actual program run

print('Hello, welcome to Icon Processing.')
print()
print('Please have your icon ready.  You will be asked to enter your 100 1s and 0s in groups of 10.')
print('\t"1s" will be interpreted as a filled pixel.')
print('\t"0s" will be interpreted as a blank pixel.')
input("Press ENTER when you are ready to continue.")
print()
print('Remember: This program requires you enter your numbers without any spaces, tabs, or commas')

data = read()
convert(data)

inverted = input("Invert? (Y/N): ")

if inverted.upper() == 'Y':
    invertedData = invert(data)
    display(invertedData)
else:
    display(data)