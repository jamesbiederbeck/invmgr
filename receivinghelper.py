import csv
import os
from pprint import pprint
from inventory import Inventory
from counthelper import getcountsfromfile


def writeupdate(csvrows):
    """Accepts a list of items,  writes a tsv file.
    """    
    #<-------Down here, output is WRITTEN---------------->
    print("writing CSV file...")
    filename = "receiveditems.tsv"
    with open(filename,'w') as f:
        print("saving updated inventory to",os.getcwd())
        fieldnames = [
            "PARTNUMBER", "ALTPARTNUMBER","DESCRIPTION1","STOCKONHAND"
            ]
        writer = csv.DictWriter(f,fieldnames=fieldnames,dialect='excel-tab')
        writer.writeheader()
        for row in csvrows:
            writer.writerow(row)
        print("Wrote file of received items at ", os.getcwd()+"\\"+filename)
        print("you can now import that to your POS.")


def main(verbose=False):
    inv = Inventory("inventory.tsv")
    output = []
    itemsnotfound = []
    receivedcountsdict = getcountsfromfile()
    print()
    print("It looks like you scanned these items:")
    for each in receivedcountsdict.keys():
        item = inv.findrecord(each)
        if not item:#Item wasn't found
            itemsnotfound.append(each)
            continue#skip adding the item to the list

        receivedquantity = receivedcountsdict[each]
        stockonhand = float(item["STOCKONHAND"])
        if stockonhand < 0:
            stockonhand = 0
        row = {}
        row["PARTNUMBER"] = item["PARTNUMBER"]
        row["ALTPARTNUMBER"] = item["ALTPARTNUMBER"]
        row["DESCRIPTION1"] = item["DESCRIPTION1"]
        row["STOCKONHAND"] = str(stockonhand+receivedquantity)
        print("    ",end='')
        print(row["DESCRIPTION1"],"x",row["STOCKONHAND"])
        output.append(row)
    print("I couldn't find these items:")
    for each in itemsnotfound:
        print(each,"x",receivedcountsdict[each])
    print(
        "I don't expect you to know what those numbers mean, so google them "+
        "if you would like to know what items those are. "
    )
    #foo = input("Press Control-C to  cancel, or enter to continue")
    writeupdate(output)
    print("update written")




if __name__ == "__main__":
    main()
else:
    print(__name__)
    