#!/usr/bin/env python3

# Theodore Lindsey
# KUID: 2620216

# TODO:
# * deal with numerical attributes (convert them to a number of binary attributes)
# * get '-' attribute values working in findAVBlocks and findCaracteristicSets
# * implement MLEM2

import os

class Entry:
    def __init__(self, decision, attributes):
        self.decision = decision # stores the decision value for the case
        self.attributes = attributes # stores the value for each attribute for the case
        self.AVmembership = {} # tracks which [(a,v)] the case belongs to on an attribute-by-attribute basis
        
class Header:
    def __init__(self, decision, attributes):
        self.decision = decision # stores the name of the decision
        self.attributes = attributes # stores the names of each attribute
        self.decisionValues = [] # stores all the decision values
        self.attributeValues = {} # stores the values for each attribute
        self.attributeType = {} # stores if each attribute is numerical or symbolic
        self.goals = {} # stores concepts for each decision
    
def isnum(string):
    parts = string.split(".")
    
    if len(parts) == 1 :
        if parts[0].isdigit():
            return True
    elif len(parts) == 2:
        if parts[0].isdigit and parts[1].isdigit():
            return True
    
    return False
        
def findAttributeValues(header, table):
    values = {}
    for attribute in header.attributes:
        for entry in range(len(table)):
            #print(entry.attributes)
            if attribute not in values:
                values[attribute] = []
            if table[entry].attributes[attribute] not in ["*", "?", "-"] + values[attribute]:
                values[attribute].append(table[entry].attributes[attribute])
        
    for attribute in values:
        if isnum(values[attribute][0]):
            header.attributeType[attribute] = "numerical"
        else:
            header.attributeType[attribute] = "symbolic"
            
        header.attributeValues[attribute] = values[attribute]
        
    for entry in range(len(table)):
        if (table[entry].decision not in header.decisionValues):
            header.decisionValues.append(table[entry].decision)

def setGoals(header, table):
    for entry in range(len(table)):
        if table[entry].decision not in header.goals:
            header.goals[table[entry].decision] = []
        header.goals[table[entry].decision].append(entry)
            
def findAVBlocks(header, table):
    avblocks = {}
    
    for attribute in header.attributes:
        for entry in range(len(table)):
            if table[entry].attributes[attribute] == "*":
                for value in header.attributeValues[attribute]:
                    if attribute + " " + value not in avblocks:
                        avblocks[attribute + " " + value] = []
                    avblocks[attribute + " " + value].append(entry)
            elif table[entry].attributes[attribute] == "-":
                print("Still need to deal with concept-based lost values")
            elif table[entry].attributes[attribute] != "?":
                if (attribute + " " + table[entry].attributes[attribute]) not in avblocks:
                    avblocks[attribute + " " + table[entry].attributes[attribute]] = []
                avblocks[attribute + " " + table[entry].attributes[attribute]].append(entry)
            
            
    return avblocks
    
def findCaracteristicSets(header, table, avblocks):
    characteristicSets = {}
    universe = [x for x in range(len(table))]
        
    for entry in range(len(table)):
        for attribute in header.attributes:
            if entry not in characteristicSets:
                characteristicSets[entry] = set(universe)
                
            if table[entry].attributes[attribute] not in ["*", "?", "-"]:
                characteristicSets[entry] = characteristicSets[entry].intersection(avblocks[attribute + " " + table[entry].attributes[attribute]])
                    
            elif table[entry].attributes[attribute] == "-":
                print("Still need to deal with concept-based lost values")
                
    return characteristicSets
    
def fileChoice():
    filelist = []
    for file in os.listdir("./"):
        if file.endswith(".txt"):
            filelist.append(file)
            
    print("Which file would you like to use?")
    for index,file in enumerate(filelist):
        print(str(index) + " - " + str(file))
    print(str(len(filelist)) + " - Manual filename entry")
    print(str(len(filelist)+1) + " - Exit")
    choice = input("> ")
    
    while (not choice.isdigit()) or (int(choice) not in range(len(filelist) + 2)):
        choice = input("Invalid selection, please try again\n> ")
    
    if int(choice) == len(filelist):
        choice = input("Please enter the desired filename:\n>")
        return choice
        
    elif int(choice) == len(filelist)+1:
        quit()
    
    else:
        print("OK, we'll use " + str(filelist[int(choice)]))
        
        return filelist[int(choice)]
        
    '''print("OK, we'll use " + str(filelist[4]))
    return filelist[4]'''
    
def approxMethodChoice():
    print("\nWhich approximation method would you like to use?")
    print("1 - Singleton")
    print("2 - Subset")
    print("3 - Concept")
    print("4 - Exit")
    choice = input("> ")
    
    while choice not in ["1", "2", "3", "4"]:
        print("Invalid selection. Please enter 1, 2, 3, or 4.")
        choice = input("> ")
        
    if choice == "4":
        quit()
        
    return int(choice)
    
def getAlpha():
    print("\nEnter the value you would like to use for alpha")
    alpha = input("> ")
    
    while not isnum(alpha) or (float(alpha) > 1 or float(alpha) <= 0):
        print("Invalid choice for alpha.  Please enter a float on the interval (0,1].")
        alpha = input("> ")
        
    return alpha

def parseFile(filename):
    file = open(filename, 'rU')
    
    counter = 0
    header = []
    table = {}
    row = []
    
    modes = ["reading header", "still reading line", "finished reading line"]
    mode = "waiting for header"
    for line in file:
        line = line.split()
        if line == []:
            continue
        elif (line[0][0] == "<") or (line[0][0] == "!"):
            continue
        elif (line[0][0] == "[") or (mode == modes[0]):
            header += [x for x in line if (x not in ["]","["])]
            
            if line[-1][-1] == "]":
                mode = modes[2]
            else:
                mode = modes[0]
                
        elif mode == modes[2]:
            row = line
            if len(row) < len(header):
                mode = modes[1]
            else:
                mode = modes[2]
                
                attributes = {}
                for attribute in range(len(row)-1):
                    attributes[header[attribute]] = row[attribute]
                    
                table[counter] = Entry(row[-1], attributes)
                counter += 1
                
                row = []
                
        elif mode == modes[1]:
            row += line
            if len(row) < len(header):
                mode = modes[1]
            else:
                mode = modes[2]
                
                table[counter] = Entry(row[-1], attributes)
                counter += 1
                
                row = []
    file.close()
    
    header = Header(header[-1], header[:-1])
             
    return (header, table)
    
def printOutput(str, file, tofile):
    if tofile:
        file.write(str)
        
def printTable(header, table, tofile = True):

    # decide if we're writing to a file.  if so, set that up.
    if tofile:
        output = open('output.txt', 'w+')
    else:
        output = ""
    
    # output the header 
    for attribute in header.attributes:
        print(attribute.ljust(15," "), end="")
        printOutput(attribute.ljust(15," "), output, tofile)
        
    print(header.decision)
    printOutput(header.decision + "\n", output, tofile)
        
    # output a newline character
    # print()
    # printOutput("\n", output, tofile)
    
    # output the entries
    for entry in range(len(table)):
        for attribute in header.attributes:
            print(table[entry].attributes[attribute].ljust(15," "), end="")
            printOutput(table[entry].attributes[attribute].ljust(15," "), output, tofile)
            
        print(table[entry].decision.ljust(15," "))
        printOutput(str(table[entry].decision.ljust(15," ")) + "\n", output, tofile)
        
        
    if tofile:
        output.close()

def singletonApprox(header, table, characteristicSets, alpha):
    approximations = {}
    for entry in range(len(table)):
        for decision in header.decisionValues:
            if decision not in approximations:
                approximations[decision] = []
                
            if len(set(header.goals[decision]).intersection(characteristicSets[entry])) / len(characteristicSets[entry]) >= alpha:
                approximations[decision].append(entry)
                
    return approximations
    
def subsetApprox(header, table, characteristicSets, alpha):
    approximations = {}
    for entry in range(len(table)):
        for decision in header.decisionValues:
            if decision not in approximations:
                approximations[decision] = []
                
            if len(set(header.goals[decision]).intersection(characteristicSets[entry])) / len(characteristicSets[entry]) >= alpha:
                approximations[decision] += [x for x in characteristicSets[entry] if x not in approximations[decision]]
                
    return approximations
    
def conceptApprox(header, table, characteristicSets, alpha):
    approximations = {}
    for entry in range(len(table)):
        for decision in header.decisionValues:
            if entry not in header.goals[decision]:
                continue
                
            if decision not in approximations:
                approximations[decision] = []
                
            if len(set(header.goals[decision]).intersection(characteristicSets[entry])) / len(characteristicSets[entry]) >= alpha:
                approximations[decision] += [x for x in characteristicSets[entry] if x not in approximations[decision]]
                
    return approximations
        
def MLEM2(header, table, approximations):
    print("coming soon")
        
# do the stuff here:
file = fileChoice() # ask which file to use
approxMethod = approxMethodChoice() # ask which approximation method to use
alpha = getAlpha() # ask what alpha should be
(header, table) = parseFile(file) # read the file into a table and gather info about the attributes
setGoals(header, table) # figure out what the goals should be
findAttributeValues(header, table) # figure out what the values for each attribute are
avblocks = findAVBlocks(header, table) # figure out what the [(a,v)] blocks are
characteristicSets = findCaracteristicSets(header, table, avblocks) # figure out what the k_A(x) sets are
if approxMethod == 1: # compute the singleton approximations given the above alpha
    approximations = singletonApprox(header, table, characteristicSets, 1)
elif subsetApprox == 2: # compute the subset approximations given the above alpha
    approximations = singletonApprox(header, table, characteristicSets, 1)
elif conceptApprox == 3: # compute the concept approximations given the above alpha
    approximations = singletonApprox(header, table, characteristicSets, 1)

    
MLEM2(header, table, approximations)