'''
This script checks for the difference in two text files, and generates two files, one with only the differences, and on with the entirety of file 1 with differences highlighted.
'''
#Import packages
import argparse
import difflib

#Function takes a string and a color, and highlight the string that color when printing to files
def highlight(line,color):
    #return '<span style=' + '\"color:' + color + '"\>' + line + '</span>'
    return "<font color=" + color + ">" + line + "</font>"

#Get files from user
args  = argparse.ArgumentParser()
args.add_argument("-o", "--original_file", required = True, help="Name of Original File")
args.add_argument("-u", "--updated_file", help="Name of Updated File",default="None")
args = vars(args.parse_args())

file_1 = args['original_file']
file_2 = args['updated_file']

#Read in text from files
with open(file_1) as f_1:
    text_1 = f_1.readlines()
with open(file_2) as f_2:
    text_2 = f_2.readlines()

#Use difflib to find and highlight differences
compared_text = difflib.unified_diff(text_1,text_2,fromfile='file_1',tofile='file_2',lineterm='')
out_text = []
for line in compared_text:
    out_text.append(line)

#Highlight out_text appropriately and write to file
out_sub_file = open("subtractions.txt","w+")
out_add_file = open("additions.txt","w+")
out_compare_file = open("comparison.txt","w+")

for line in out_text:
    if line[0] == '-':
        out_sub_file.write(line)
    elif line[0] == '+':
        out_add_file.write(line)
    out_compare_file.write(line)
    print(line)
