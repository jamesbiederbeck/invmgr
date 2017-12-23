# coding: utf-8

import csv
from pprint import pprint
delimiter = "\t"#assume tab-separated file, because that's my use case

class Inventory():
    """this is an abstraction of an inventory file
    It contains a csv reader at Inventory.reader"""
    def __init__(self,file):
        self.f = open(file)
        print("Loading file",file)
        self.reader = csv.DictReader(self.f,delimiter=delimiter)#probably "," or "\t"
        print("Found headers in inventory file:")
        print(self.reader.fieldnames)
        self.items = list(self.reader)
        print("found", len(self.items), "items")
        #self.close()#still trying to decide if necessary
    def __len__(self):
        return len(self.items)
    def getDialect(self):
        self.sniffer = csv.sniffer()
    def close(self):
        self.f.close()
    def findrecord(self, partnumber):
        """takes a part number, returns the inventory entry for that item"""  
        for row in self.items:
            if row["PARTNUMBER"]==partnumber:
                return row
            if row["ALTPARTNUMBER"]==partnumber:
                return row
        #assume that if execution reached this point, nothing was found.
        print("Could not find record,",partnumber)
        return None

def getcounts(filepath = ""):
    """This will read a list of barcodes, and flatten to a list of
        all the barcodes and how many times each one is in the list."""
    while not filepath: #ensure a filepath gets specified
        print("This will read inventory counts from a list of barcodes/SKU's.")
        filepath = input("Enter the path to the file you would like to parse.")
        
    with open(filepath) as f:#open the file
        data = f.read()
        data.rstrip()#remove trailing newlines
        data.split("\n")#split the string into a list of lines

    #initialize dictionary of part numbers and counts
    countsdict ={}

    #This goes through the list of part numbers, and makes sure each has an
    #entry in the dictionary.
    for line in set(data):
        countsdict[line] = 0 

    #Increment count for each instance of the sku in the list of part numbers
    #found
    for line in data:
        #countsdict[line.split("\t")[0]] +=1
        countsdict[line]+=1
    print("Found",len(countsdict),"items in the barcode list!")

    return countsdict

def listupdateditems(inventory1, inventory2, field = ""):
    """Compare 2 inventories, return list of partnumbers with different fields
    Optionally, this function can look at only one field for updates, eg 
    "STOCKONHAND"
    Returns a list of partnumbers
    """
    if len(field):
        assert field in inventory1.reader.fieldnames#validate fieldname
        assert field in inventory2.reader.fieldnames
    differentitems = []
    similaritemcounter = 0
    for item1 in inventory1.items:
        item2 = inventory2.findRecord(item1["PARTNUMBER"]) #find an equivalent record
        assert item2 != None
        if len(field):#if a field to compare is specified
            if item1[field] != item2[field]:#compare the fields for the 2 items
                print(item1[field],item2[field])
                differentitems +=item2["PARTNUMBER"]
            else:
                #print("similar item,", item1["PARTNUMBER"],item1["DESCRIPTION1"])
                similaritemcounter +=1
        else:
            for fieldname in inventory1.reader.fieldnames:
                if item1[fieldname] != item2[fieldname]:
                    differentitems += item2
                else:
                    similaritemcounter +=1
    
    # print("Found,",differentitems,"different items")
    print("Different items",len(differentitems))
    print("Similar items", similaritemcounter)
    print("That's out of ",len(inventory2.items),"items in inventory 2")
    return differentitems

def getexclusionsfromfile(filepath = ""):
    """This will read a list of partnumbers from file"""
    while not filepath: #ensure a filepath gets specified
        print("This script accepts a list of part numbers to not touch")
        filepath = input("Enter the path to the file to load, or 'skip'")
        if filepath == 'skip':
            return ""
        
    with open(filepath) as f:#open the file
        data = f.read()
        data.rstrip()#remove trailing newlines
        data.split("\n")#split the string into a list of lines
        
    return data

def zerostockforallitems(inventory, countsdict, exclusions=[]):
    """Iterate through inventory, fill countsdict, setting items to 0
    Takes optional argument exclusions
    """
    for row in inventory.items:
        if row["PARTNUMBER"] not in exclusions:
            if row["ALTPARTNUMBER"] not in exclusions:
                countsdict[row["PARTNUMBER"]] = 0

def main():
    print("Welcome to new and improved inventory manager!")
    inv = Inventory("test-eoy2017preupdate.tsv")
    inv2 = Inventory("test-eoy2017postscan.tsv")
    countsdict = getcounts("barcodefile.txt")
    exclusions = listupdateditems(inv, inv2, "STOCKONHAND")
    print(len(exclusions))
    #add entries to counts dict to zero out items, by modifying the list
    #in place
    zerostockforallitems(inv, countsdict, exclusions)
    items ={}# this is a dict of alt partnumbers as a secondary lookup table
    output = []#list of dicts, unique
    i = 0

    #Generate dicts for items' partnumber/altpartnumber pairings
    for row in inv.items: 
        items[row["PARTNUMBER"]] = row["ALTPARTNUMBER"]
    #print(row["DESCRIPTION1"])
        i+=1 #count iterations because csv.reader has no length method
    print("Found",i,"items in inventory!")
    print("Parnumber/Altpartnumber assignments loaded")
    
    #The next block is where output actually gets generated
    #Go through list of counts, and make a row consisting
    #of partnumber, altpartnumber, stockonhand
    #print(items)
    itemsnotfound = []
    for key,value in countsdict.items():
        stockonhand = value#stock on hand        
    #Assign the partnumber and altpartnumber fields
        item = inv.findrecord(key)
        if item:
            partnumber = item["PARTNUMBER"]
            altpartnumber = item["ALTPARTNUMBER"]
        else:
            #clear the variables
            partnumber = None
            altpartnumber = None 
            # print("Item not found for partnumber ",key)
            itemsnotfound.append(key)
            continue #Skip adding the part data to the output

        row = {
            "PARTNUMBER":partnumber,
            "ALTPARTNUMBER":altpartnumber,
            "STOCKONHAND":stockonhand
            }
        print(row)
        output.append(row)
    print()# vertical space
    print("Here's the output")
    pprint(output)
    
    #<-------Down here, output is WRITTEN---------------->
    print("writing CSV file...")
    with open("updated-inventory",'w') as f:
        fieldnames = ["PARTNUMBER", 'ALTPARTNUMBER','STOCKONHAND']
        writer = csv.DictWriter(f,fieldnames=fieldnames,dialect='excel-tab')
        writer.writeheader()
        for row in output:
            writer.writerow(row)
        print("Success")

if __name__ == "__main__":
    print("running main")
    main()