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
