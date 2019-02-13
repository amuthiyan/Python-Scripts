import argparse

#Define necessary functions
#Read the data into the program as a list of records
def ReadIndex(filename):
    file = open(filename,'r')
    record_index = []
    doc = file.readlines()
    for line in doc:
        line = line.strip('\n ')
        line_lst = line.split(' ')
        record_index.append(line_lst)
    return record_index

#Create a frequency index for each of the items
def getOccIndex(record_index):
    freq_index = {}
    for record_num in range(len(record_index)):
        for item in record_index[record_num]:
            if item not in freq_index:
                freq_index[item] = []
                freq_index[item].append(record_num)
            else:
                freq_index[item].append(record_num)
    return freq_index

#Creates an empty list to fill in with frequent itemsets
def getFreqSets(num_terms):
    freq_itemsets = []
    for i in range(0,num_terms+1):
        temp = []
        freq_itemsets.append(temp)
    return freq_itemsets

#Calculates the support of every itemset
def GetSup(itemset,occ_index,d_sup_vals):
    if tuple(itemset) in d_sup_vals:
        return d_sup_vals[tuple(itemset)]
    inv_lists = []
    for term in itemset:
        inv_lists.append(occ_index[term])
    else:
        sup = len(Intersect(inv_lists))
        d_sup_vals[tuple(itemset)] = sup
    return sup

#Returns the intersect of the terms of inv_lists
def Intersect(inv_lists):
    sect_terms = inv_lists[0]
    for term in inv_lists:
        sect_terms = set(sect_terms).intersection(term)
    return sect_terms

#Determine if two sets need to be joined
def NeedJoin(set1,set2):
    for i in range(0,len(set1)-1):
        if set1[i] != set2[i]:
            return False
    return True

#Joins two sets
def Join(set1,set2):
    set3 = list(set1)
    set3.append(set2[-1])
    return set3

#Read in the mapping file to a dictionary
def getCodeMap(code_filename):
    code_map = {}
    file = open(code_filename,'r')
    codes = file.readlines()
    for code in codes:
        code = code.split(" ")
        code_map[code[1].strip("\n")] = code[0]
    return code_map

#Returns list of item codes from the code map
def parseCodeMap(code_map):
    item_codes = []
    for name in code_map:
        item_codes.append(code_map[name])
    return item_codes

#Returns a clean index of transactions
def getCleanIndex(unclean_index,item_codes,code_map):
    clean_index = []
    for record_num in range(len(unclean_index)):

        #Split on ';' if needed
        if len(unclean_index[record_num]) == 1:
            if ';' in unclean_index[record_num][0]:
                unclean_index[record_num] = unclean_index[record_num][0].strip("\n").split(';')[0:-1]

        #Replace item names with item codes
        for item_num in range(len(unclean_index[record_num])):
            if unclean_index[record_num][item_num] in code_map:
                unclean_index[record_num][item_num] = code_map[unclean_index[record_num][item_num]]

        #Delete records with invalid item codes
        num_invalid = 0
        for item_num in range(len(unclean_index[record_num])):
            if unclean_index[record_num][item_num] not in item_codes:
                num_invalid += 1
        if num_invalid == 0:
            clean_index.append(unclean_index[record_num])
    return clean_index

#Get inputs from command line in order:
args  = argparse.ArgumentParser()
args.add_argument("-i", "--input_file", required = True, help="Name of Input File")
args.add_argument("-m", "--mapping_file", help="Name of mapping File",default="None")
args.add_argument("-s", "--min_support", required = True, help="Minimum support count")
args.add_argument("-o", "--output_file", required = True, help="Name of Output File")
args = vars(args.parse_args())

in_filename = args["input_file"]
map_filename = args["mapping_file"]
min_sup = int(args["min_support"])
out_filename = args["output_file"]

#Case if file is clean (mapping file not given):
if map_filename == 'None':
    #Read the file in as a list of transactions
    record_index = ReadIndex(in_filename)
else:
    code_map = getCodeMap(map_filename)
    item_codes = parseCodeMap(code_map)
    unclean_index = ReadIndex(in_filename)
    record_index = getCleanIndex(unclean_index,item_codes,code_map)

#Get the occurrence based index
occ_index = getOccIndex(record_index)

#Get the total number of records and number of unique terms
num_records = len(record_index)
num_unique_items = len(occ_index)

#Create a dictionary of itemsets and their support values
d_sup_vals = {}

#Initialise empty set of frequent itemsets
freq_itemsets = getFreqSets(num_unique_items)

#Find all the frequent 1 itemsets
for item in occ_index:
    #print(item)
    itemset = [item]
    item_sup = GetSup(itemset,occ_index,d_sup_vals)
    #print(item_sup)
    if item_sup >= min_sup:
        freq_itemsets[0].append(itemset)

#Find frequent 2 to K-itemsets
for k in range(1,num_unique_items+1):
    prev_itemsets = freq_itemsets[k-1]
    n = len(prev_itemsets)
    for i in range(1,n-1):
        for j in range(i+1,n):
            set1 = prev_itemsets[i]
            set2 = prev_itemsets[j]
            if NeedJoin(set1,set2):
                set3 = Join(set1,set2)
                if GetSup(set3,occ_index,d_sup_vals)>=min_sup:
                    freq_itemsets[k].append(set3)
    if len(freq_itemsets) == 1:
        break

#Put the results into the output file
course_info = "CS634-101 Data Mining"
my_name = "Aneesh Muthiyan"
due_date = "10/29/2018"
purpose = "To separate the transactions into frequent itemsets"

out_file = open(out_filename,"w")
out_file.write("Course: "+course_info+"\n")
out_file.write("Name: "+my_name+"\n")
out_file.write("File Name: "+out_filename+"\n")
out_file.write("Due Date: "+due_date+"\n")
out_file.write("Program Purpose: "+purpose+"\n")
for k in range(len(freq_itemsets)):
    for itemset in freq_itemsets[k]:
        out_set = ""
        for item in itemset:
            out_set += item
            out_set += " "
        out_set += "("+str(d_sup_vals[tuple(itemset)])+")"
        out_file.write(out_set+"\n")
        print(out_set)
out_file.close()
