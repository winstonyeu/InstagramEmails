# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
import Configuration
from random import randint
import requests, csv, time
from instagram.bind import InstagramAPIError
import re, os.path, sys
from unidecode import unidecode

import threading
import simplejson

config = Configuration.Configuration('config.ini')
numoftoken = int(len(config.dictionary) * 0.5)

access_token = []
client_id    = []   
api          = []

for num in range(numoftoken):
    access_token.append(config.dictionary['accesstoken' + str(num+1)])
    client_id.append(config.dictionary['clientid' + str(num+1)])
    api.append(InstagramAPI(access_token=access_token[num]))
  
# access_token = config.dictionary['accesstoken']
# client_id    = config.dictionary['clientid']
# api = InstagramAPI(access_token=access_token)
 
class Keywords():
    def __init__(self, category):
        filename = open(category+'.txt', 'r')
        self.words = filename.read().splitlines()
        filename.close()
 
        self.currentTag = ""
     
    # Returns number to words in text file in array terms (Length - 1)
    def WordsLength (self):
        return len(self.words) - 1
     
    # Generates random index from the number of words
    def RandomWords (self):
        listNum = randint(0, self.WordsLength())
        print("Keyword: %s" % self.words[listNum])
        return self.words[listNum]
         
class AutoLoveTag: 
    def __init__(self, category):
        self.medialist = []
        self.filename = "users.csv"
        self.USERNAMEFILE = "users.txt"
        self.category = category
         
    def DecodeJSONData(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        response = requests.get(url, headers = headers)
        #print(response.headers['x-ratelimit-remaining'])
        if response.status_code == 429:
            raise InstagramAPIError("429", "Rate Limit Exceed", "Rate limit exceeded")
        
        while True:
            try:
                decodedData = response.json()
                break
            except simplejson.scanner.JSONDecodeError:
                continue
        return decodedData
     
    def writeToCSV(self, filename, data):
        if not os.path.exists(self.category):
            os.makedirs(self.category)
        filename = self.category+"/"+filename+".csv"
        fieldnames = ['user', 'followerscount', 'description', 'link', 'tag', 'email']
        csvwriter = csv.DictWriter(open(filename,'a'), delimiter=',', fieldnames=fieldnames, lineterminator="\n")
        csvwriter.writerow(data)
        #print("Done writing")
     
    def WriteToFile(self, filename, text):
        filename = self.category+"/filecheck/"+filename+".txt"
        userFile = open(filename, 'a')
        userFile.write(text + "\n")
        userFile.close()
     
    def ClearFile(self, filename):
        filename = self.category+"/filecheck/"+filename+".txt"
        open(filename, 'w').close()
         
    def CheckExistenceInFile(self, filename, text):
        if not os.path.exists(self.category):
            os.makedirs(self.category)
        if not os.path.exists(self.category+"/filecheck"):
            os.makedirs(self.category+"/filecheck")
        filename = self.category+"/filecheck/"+filename+".txt"
        open(filename, 'a')
        userFile = open(filename, 'r')
        for text_in_file in userFile.read().splitlines():
            if text == text_in_file:
                userFile.close()
                return True  
              
        userFile.close()    
        return False
         
    def getNextUrl(self, url):
        r = requests.get(url)
        r = r.json()
        return r['pagination']['next_url']
     
    def getEmail(self, s):
        r = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
        email = re.search(r, s)
        if email == None:
            return None
         
        email = email.group(0)
        return email
     
    def Main(self, thread, keywords):
        tag_name = keywords.words[thread]
        usercount = 0
        userdict = {}
           
        url = "https://api.instagram.com/v1/users/%s/?access_token=" + access_token[thread]
         
        print(tag_name + ": START")
        #self.ClearFile(tag_name)
        while True:
            try:
                medias = api[thread].tag_recent_media(count=50, tag_name=tag_name, pagination=True)
                next_url = medias[1]
                    
                while True:
                    users = self.DecodeJSONData(next_url)
                    for user in users['data']:
#                         if usercount >= 10000:
#                             breakloop = True
#                             break
                            
                        user_name = user['user']['username']
                            
                        if self.CheckExistenceInFile(tag_name, user_name):
                            continue
                            
                        user_id = user['user']['id']
                        
                        userinfo = self.DecodeJSONData(url % user_id)
                        
                        try:
                            user_followers_count = userinfo['data']['counts']['followed_by']
                            user_email = self.getEmail(userinfo['data']['bio'])
                        except KeyError:
                            continue
                            
#                         userinfo = api.user(user_id)
#                         user_followers_count = userinfo.counts['followed_by']
#                         user_email = self.getEmail(userinfo.bio)
                            
                        if user_email == None:
                            continue
                            
                        user_email = unidecode(user_email)
                            
                        try:
                            user_description = "".join(i for i in user['caption']['text'] if ord(i)<128).encode('utf-8')
                        except TypeError:
                            user_description = "No description"
                        user_link = user['link']
                            
                        userdict['user'] = user_name
                        userdict['followerscount'] = user_followers_count
                        userdict['description'] = user_description
                        userdict['link'] = user_link
                        userdict['tag'] = tag_name
                        userdict['email'] = user_email
                        self.writeToCSV(tag_name, userdict)
                            
                        usercount += 1
                            
                        print(tag_name + ": Writing to name to file -", usercount)
                        self.WriteToFile(tag_name, user_name)
                            
#                     if breakloop:
#                         breakloop = False
#                         break
                        
                    next_url = users['pagination']['next_url']
                break
            except InstagramAPIError:
                print(tag_name + ": Rate limit exceeded, waiting %s hour before continuing" % 1)
                time.sleep(3600)
                print(tag_name + ": Finished waiting, continuing...")
                continue
                
            print(tag_name + ": END")
            break   
                  
if __name__ == "__main__":
    try:
        category = sys.argv[1]
        keywords = Keywords(category)
        threads = []
        lovetag = AutoLoveTag(category)
        for thread in range(keywords.WordsLength()):
            t = threading.Thread(target=lovetag.Main, args=(thread, keywords))
            threads.append(t)
            t.start()
    except Exception as e:
        print(e)
        print("No category choosen")
        os.system("pause")
   
#     lovetag = AutoLoveTag()
#     lovetag.Main()
    






