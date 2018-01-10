def getcountsfromfile(filepath=""):
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
    countsdict = {}#{partnumber:int}
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
    