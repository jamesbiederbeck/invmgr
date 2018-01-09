from inventory import Inventory
import csv
import os


def writeupdate(csvrows):
    """Accepts a list of items,  writes a tsv file.
    """    
    #<-------Down here, output is WRITTEN---------------->
    print("writing CSV file...")

    with open("receiveditems.tsv",'w') as f:
        print("saving updated inventory to",os.getcwd())
        fieldnames = [
            "PARTNUMBER", "ALTPARTNUMBER","DESCRIPTION1","STOCKONHAND"
            ]
        writer = csv.DictWriter(f,fieldnames=fieldnames,dialect='excel-tab')
        writer.writeheader()
        for row in csvrows:
            writer.writerow(row)
        print("Success")

def main():
    inv = Inventory("inventory.tsv")
    receiveditems = []
    with open("receivedscan.txt") as f:
        scannedbarcodes = f.readlines()
    for each in scannedbarcodes:
        each = each.rstrip()#get rid of newlines
        item = inv.findrecord(each)
        row = {}
        row["PARTNUMBER"] = item["PARTNUMBER"]
        row["ALTPARTNUMBER"] = item["ALTPARTNUMBER"]
        row["DESCRIPTION1"] = item["DESCRIPTION1"]
        row["STOCKONHAND"] = str(float(item["STOCKONHAND"])+1)
        print(row)
        receiveditems.append(row)
    writeupdate(receiveditems)



if __name__ == "__main__":
    main()
else:
    print(__name__)
    