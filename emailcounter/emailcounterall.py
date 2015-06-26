import csv
import os
from os import listdir
from os.path import isfile, join
import re, time

category = ["artistcovers", "cats", "cleaneating", "dogs", "fashion", "females", "food", "gym", 
            "mothers", "music", "photographers", "travel", "videographers", "vlogs", "yoga"]

def userCount(folder, filename):
    with open("../" + folder + "/" + filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        num_lines = sum(1 for row in csvreader if row[5].strip())
        csvfile.close()
        return num_lines
    
if __name__ == '__main__':

    dirs = [d for d in os.listdir('../') if os.path.isdir(os.path.join('../', d))]
    
    totalnum = 0
    wait = 3
    
    for cat in category:
        for dir in dirs:
            if dir == cat:
                files = [ f for f in listdir("../" + dir) if isfile(join("../" + dir,f)) ]
                for file in files:
                    p = re.compile(r'\b([.]\w+)')
                    resp = p.search(file)
                    if resp.group() == ".csv":
                        totalnum += userCount(cat, file)
  
    print("Total num of emails:", totalnum)
    print("Closing in", wait, "seconds")
    time.sleep(wait)
        
        
        