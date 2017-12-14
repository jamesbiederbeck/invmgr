
# coding: utf-8

# In[8]:

import csv
from pprint import pprint
delimiter = "\t"

class Inventory():
    def __init__(self,file):
        self.f = open(file)
        print("Loading file",file)
        reader = csv.DictReader(self.f,delimiter=delimiter)#probably "," or "\t"
        print("Found fields in database:")
        print(reader.fieldnames)
        self.reader=reader
    def getDialect(self):
        self.sniffer = csv.sniffer()

    def close():
        self.f.close()

    def findRecord(self, partnumber):
        #takes a part number, returns the inventory entry for that item
        for row in self.reader:
            if row["PARTNUMBER"]==partnumber:
                return row
            if row["ALTPARTNUMBER"]==partnumber:
                return row
        #assume that if execution reached this point, nothing was found.
        #print("Could not find record,",partnumber)
        print("none found")
        return None

def getCounts(filepath = ""):
    """This will read a list of barcodes, and flatten to a list of
        all the barcodes and how many times each one is in the list."""
    while not filepath: #ensure a filepath gets specified
        print("This will read inventory counts from a list of barcodes/SKU's.")
        filepath = input("Enter the path to the file you would like to parse.")
        
    with open(filepath) as f:#open the file
        data = f.read().split("\n")#chop the string into a list of lines

    #initialize dictionary of part numbers and counts
    countsdict ={}

    #This goes through the list of part numbers, and makes sure each has an
    #entry in the dictionary. Inefficient, but not wasteful enough to matter
    #at this scale.
    for line in data:
        #here I get only the first column, since I added timestamps to counts list
        #countsdict[line.split("\t")[0]] = 0 
        countsdict[line] = 0 

    #Increment count for each instance of the sku in the list of part numbers
    #found
    for line in data:
        #countsdict[line.split("\t")[0]] +=1
        countsdict[line]+=1
    print("Found",len(countsdict),"items in the barcode list!")

    return countsdict

def process(row):
    #because paladin associates two or more partnumbers with
    #everything, we have to check each one agaisnt the update dict
        if row[id_field] in updatedict:
            row["STOCKONHAND"]=str(countsdict[row[id_field]] )


# In[9]:

def main():
    inv = Inventory("inventory04-19-17")
    countsdict = getCounts("barcodefile.txt")
    items ={}# this is a dict of alt partnumbers as a secondary lookup table
    output = []#This will eventually be a list of dicts; primary key:partnumber
    i = 0

    #Generate dicts for items' partnumber/altpartnumber pairings
    for row in inv.reader: 
        items[row["PARTNUMBER"]] = row["ALTPARTNUMBER"]
#         print(row["DESCRIPTION1"])
        i+=1 #count iterations because csv.reader has no length method
    print("Found",i,"items in inventory!")
    print("Parnumber/Altpartnumber assignments loaded")
    #and now we reverse the key/value assignment using a list comprehension
    #itemsbyaltpartnumber = {v: k for k, v in items}
    
    #The next block is where output actually gets generated
    
    #Go through list of counts, and make a row consisting
    #of partnumber, altpartnumber, stockonhand
    #print(items)
    itemsnotfound = []
    for key,value in countsdict.items():
        
#         Assign the partnumber and altpartnumber fields
        if key in items.keys():
            print("Partnumber found")
            partnumber = key
            altpartnumber = items[key]
        elif key in items.values():
            print("Item Found by ALTPARTNUMBER")
            #look for the item among items' altpartnumbers
            for partnumber, altpartnumber in items.items():
                if altpartnumber == key:
                    #found the item, so we can stop
                    #NOTE: partnumber and altpartnumber have been assigned here
                    #as part of the for loop, but explicit is better than explicit
                    # so I just do the assignment anyways.
                    partnumber = partnumber
                    altpartnumber = altpartnumber
                    break
        else:
            #clear the variables
            partnumber = None
            altpartnumber = None 
            print("Item not found for partnumber ",key)
            itemsnotfound.append(key)
            continue

        count = value#Got assigned at the top of this for loop

        row = {
            "PARTNUMBER":partnumber,
            "ALTPARTNUMBER":altpartnumber,
            "STOCKONHAND":count
            }
        print(row)
        output.append(row)
    print()# vertical space
    print("Here's the output")
    pprint(output)

    print("writing CSV file...")
    with open("updated-inventory",'w') as f:
        fieldnames = ["PARTNUMBER", 'ALTPARTNUMBER','STOCKONHAND']
        writer = csv.DictWriter(f,fieldnames=fieldnames,dialect='excel-tab')
        writer.writeheader()
        for row in output:
            writer.writerow(row)
        print("Success")
        print("Items not found:")
if __name__ == "__main__":
    main()
    

