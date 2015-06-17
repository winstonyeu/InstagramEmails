import csv
import os
from os import listdir
from os.path import isfile, join
import re, time

def userCount(folder, filename):
    with open(folder + "/" + filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        num_lines = sum(1 for row in csvreader if row[5].strip())
        csvfile.close()
        return num_lines
    
if __name__ == '__main__':
    while True:
        category = input('Enter category: ')

        try:
            onlyfiles = [ f for f in listdir(category) if isfile(join(category,f)) ]
            break
        except FileNotFoundError:
            os.system('cls')
            print("Invalid category, try again")
        
    totalnum = 0
    wait = 3
    
    for file in onlyfiles:
        p = re.compile(r'\b([.]\w+)')
        resp = p.search(file)
        if resp.group() == ".csv":
            totalnum += userCount(category, file)
  
    print("Total num of emails:", totalnum)
    print("Closing in", wait, "seconds")
    time.sleep(wait)
        
        
        