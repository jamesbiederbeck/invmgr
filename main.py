# coding: utf-8

import os
import csv
from inventory import Inventory
from pprint import pprint
DELIMITER = "\t"#assume tab-separated file, because that's my use case

def getcounts(filepath = ""):
    """This will read a list of barcodes, and flatten to a list of
        all the barcodes and how many times each one is in the list."""
    while not filepath: #ensure a filepath gets specified
        print("This will read inventory counts from a list of barcodes/SKU's.")
        filepath = input("Enter the path to the file you would like to parse.")
    with open(filepath) as f:#open the file
        data = f.read()
        data = data.rstrip()#remove trailing newlines
        data = data.split("\n")#split the string into a list of lines
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
    i = 1#I would zero index, but then we get div/0 error
    for item1 in inventory1.items:
        itemfoundbyaltpartnumber = False
        i +=1#count rows processed
        totalitems = len(inventory1.items)
        if not i%(totalitems//100):#print a period every time 1% is completed
            print(".", end = "")
        item2 = inventory2.findrecord(item1["PARTNUMBER"]) #find an equivalent record
        try:
            assert item2 != None
        except AssertionError:#sometimes partnumbers change, evidently
            itemfoundbyaltpartnumber = True
            print("item not found in inv2 by partnumber:", item1)
            item2 = inventory2.findrecord(item1["ALTPARTNUMBER"])
            print("item found by altpartnumber,",item1["ALTPARTNUMBER"])
        if len(field):#if a field to compare is specified
            if item1[field] != item2[field]:#compare the fields for the 2 items
                # print(item1[field],item2[field])
                if itemfoundbyaltpartnumber:
                    differentitems.append(item2["ALTPARTNUMBER"])
                else:
                    differentitems.append(item2["PARTNUMBER"])
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
        data = data.rstrip()#remove trailing newlines
        data = data.split("\n")#split the string into a list of lines
        data = list(set(data))
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
    inv2 = Inventory("real inventory.tsv")
    countsdict = {}
    if "barcodefile.txt" in os.listdir():
        countsdict += getcounts("barcodefile.txt")
    else:
        print("No file of updated barcodes found.")
    exclusions = []
    try: #This "try" block loads a list of partnumbers to ignore, from file
        exclusionsfromfile = getexclusionsfromfile("exclusions.txt")
        print("exclusions file found,",len(exclusionsfromfile), "entries")
        exclusions += exclusionsfromfile
    except FileNotFoundError:
        print("No exclusions file found. Continue?")
        if ("Y") not in input().lower():
            print("You didn't say yes or some variation. Exiting.")
            exit()
        else:
            print("Continuing without exclusions file")
    exclusions += listupdateditems(inv, inv2, "STOCKONHAND")#skip changed items
    exclusions += list(countsdict.keys()) #exclude items already counted
    exclusions = list(set(exclusions)) #strip non-unique items
    print(len(inv.items)-len(exclusions), "items' stock will be set to 0")
    #set counts to zero for any item in inventory that isn't exclude
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
        if item:#check if the item was found
            partnumber = item["PARTNUMBER"]
            altpartnumber = item["ALTPARTNUMBER"]
            #description1 = item["DESCRIPTION1"]
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
            #"DESCRIPTION1":description1,
            "STOCKONHAND":stockonhand
            }
        output.append(row)
    print()# vertical space

    
    #<-------Down here, output is WRITTEN---------------->
    print("writing CSV file...")
    with open("2017eoyupdate.tsv",'w') as f:
        fieldnames = ["PARTNUMBER", 'ALTPARTNUMBER','STOCKONHAND']
        writer = csv.DictWriter(f,fieldnames=fieldnames,dialect='excel-tab')
        writer.writeheader()
        for row in output:
            writer.writerow(row)
        print("Success")

if __name__ == "__main__":
    print("running main")
    main()