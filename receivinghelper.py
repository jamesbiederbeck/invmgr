from inventory import Inventory
import csv
import os
from pprint import pprint


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

def main(verbose=False):
    inv = Inventory("inventory.tsv")
    receiveditems = []
    itemsnotfound = []
    with open("receivedscan.txt") as f:
        scannedbarcodes = f.readlines()
    print()
    print("It looks like you scanned these items:")
    for each in scannedbarcodes:
        each = each.rstrip()#get rid of newlines
        item = inv.findrecord(each)
        if not item:#Item wasn't found
            itemsnotfound.append(each)
            continue#skip adding the item to the list
        row = {}
        row["PARTNUMBER"] = item["PARTNUMBER"]
        row["ALTPARTNUMBER"] = item["ALTPARTNUMBER"]
        row["DESCRIPTION1"] = item["DESCRIPTION1"]
        row["STOCKONHAND"] = str(float(item["STOCKONHAND"])+1)
        print("    ",end='')
        print(row["DESCRIPTION1"],"x",row["STOCKONHAND"])
        receiveditems.append(row)
    print("I couldn't find these items:")
    pprint(itemsnotfound)
    print(
        "I don't expect you to know what those numbers mean, so google them "+
        "if you would like to know what items those are. "
    )
    input("Press Control-C to  cancel, or enter to continue")
    writeupdate(receiveditems)



if __name__ == "__main__":
    main()
else:
    print(__name__)
    