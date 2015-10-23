class entry:
    def __init__(self, decision, attributes):
        self.decision = decision
        self.attributes = attributes

def parseFile(filename):
    file = open(filename, 'rU')
    
    header = []
    table = []
    row = []
    
    modes = ["reading header", "still reading", "finished reading"]
    mode = "waiting for header"
    for line in file:
        line = line.split()
        if line == []:
            continue
        elif line[0][0] == "<":
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
                table.append(entry(row[-1], attributes))
                
                row = []
                
        elif mode == modes[1]:
            row += line
            if len(row) < len(header):
                mode = modes[1]
            else:
                mode = modes[2]
                table.append(row)
                row = []
    file.close()
             
    return (header, table)
    
def printTable(header, table):
    
    for attribute in header:
        print(attribute.ljust(15," "), end="")
    print()
    for entry in table:
        for attribute in header[:-1]:
            print(entry.attributes[attribute].ljust(15," "), end="")
        print(entry.decision.ljust(15," "))



(header, table) = parseFile("jerzy1.txt")
printTable(header, table)