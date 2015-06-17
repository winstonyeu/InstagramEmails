import csv
import os
from os import listdir
from os.path import isfile, join
import re, time
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            p = re.compile(r'\b([.]\w+)')
            resp = p.search(file)
            if resp.group() == ".csv":
                ziph.write(os.path.join(root,file),arcname=file)
    
if __name__ == '__main__':
    zipnum = 1
    while True:
        category = input('Enter category: ')
  
        try:
            onlyfiles = [ f for f in listdir("../" + category) if isfile(join("../" + category,f)) ]
            break
        except FileNotFoundError:
            os.system('cls')
            print("Invalid category, try again")
    
    while True:
        filename = category.capitalize() + "_Zip" + str(zipnum) + ".zip"
        if os.path.isfile(filename):
            zipnum += 1
        else:
            break
    
    zipf = zipfile.ZipFile(filename, 'w')
    zipdir("../" + category + "/", zipf)
    zipf.close()
        