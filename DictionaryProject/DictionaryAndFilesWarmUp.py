def read():
    file = open('DictionaryFile.txt', 'r')
    
    names = []
    
    for line in file:
        line = line.rstrip('\n')
        names.append(line)
    
    return names

def greet(nameList):
    for name in nameList:
        print(f"Hello {name}")

names = read()
greet(names)