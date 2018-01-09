import inventory
import csv

def writeupdate(csvrows):
    """Accepts a list of items,  writes a tsv file.
    """    
    #<-------Down here, output is WRITTEN---------------->
    print("writing CSV file...")
    with open("expireditemstodiscontinue.tsv",'w') as f:
        fieldnames = [
            "PARTNUMBER", 'ALTPARTNUMBER','MAXSTOCK'
            ]
        writer = csv.DictWriter(f,fieldnames=fieldnames,dialect='excel-tab')
        writer.writeheader()
        for row in output:
            writer.writerow(row)
        print("Success")



def main():
    inv = inventory("inventory.tsv")
    expireditems = []
    with open("expiredscan") as f:
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
        expireditems.append(row)
    writeupdate(expireditems)

if __name__ == "__MAIN__":
    main()
    