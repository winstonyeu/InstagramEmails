import csv
import os
from os import listdir
from os.path import isfile, join
import re, time
import zipfile

category = ["artistcovers", "cats", "cleaneating", "dogs", "fashion", "females", "food", "gym", 
            "mothers", "music", "photographers", "travel", "videographers", "vlogs", "yoga"]

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
     
    dirs = [d for d in os.listdir('../') if os.path.isdir(os.path.join('../', d))]

    for cat in category:
        for dir in dirs:
            if dir == cat:
                while True:
                    filename = dir.capitalize() + "_Zip" + str(zipnum) + ".zip"
                
                    if os.path.isfile(filename):
                        zipnum += 1
                    else:
                        break
                    
                zipnum = 1
                zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
                zipdir("../" + dir + "/", zipf)
                zipf.close()
        
        