import csv
DELIMITER = "\t"#assume tab-separated file, because that's my use case

class Inventory():
    """this is an abstraction of an inventory file
    It contains a csv reader at Inventory.reader"""
    def __init__(self, file,):
        self.f = open(file)
        print("Loading file", file)
        self.reader = csv.DictReader(self.f, delimiter=DELIMITER)
        print("Found headers in inventory file:")
        print(self.reader.fieldnames)
        self.items = list(self.reader)
        print("found", len(self.items), "items")
        #self.close()#still trying to decide if necessary
    def getvalue(self):
        total = 0 
        for each in self.items:
            stock = float(each["STOCKONHAND"])
            if stock <= 0: #Don't count items that aren't in stock
                continue
            cost = float(each["UNITCOST"])
            total += stock * cost
        return total        
    def __len__(self):
        return len(self.items)
    def getDialect(self):
        sniffer = csv.Sniffer()
        sniffer.sniff(self)
    def close(self):
        self.f.close()
    def findrecord(self, partnumber):
        """takes a part number, returns the inventory entry for that item"""  
        for row in self.items:
            if row["PARTNUMBER"] == partnumber:
                return row
            if row["ALTPARTNUMBER"] == partnumber:
                return row
        #assume that if execution reached this point, nothing was found.
        print("Could not find record,", partnumber)
        return None
    def updateitemfield(self,partnumbers,field,value,output=[]):
        """Accepts a partnumber, altpartnumber, or list thereof, and updates
        sets the field passed to the value passed. Appends to output in place,
        and also returns output.
        """
        pass
        # if type(partnumbers) == list:
        #     for item in inv.items:

        # elif type(partnumbers) == str:
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