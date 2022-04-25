'''
CCM
Copyright (c) 2021 Gaëtan Robillard and Jolan Goulin
BSD Simplified License.
For information on usage and redistribution, and for a DISCLAIMER OF ALL
WARRANTIES, see the file, "LICENSE.txt," in this distribution.
'''

# UTILITIES FOR MONITORING
# ----------------------------------------------------------------------

from bson.json_util import dumps
import json
from datetime import datetime, timedelta
import db as d

def mongoToJson(n, filename):
    db, collection = d.dbConnect()
    cursor = collection.find().sort("_id",-1).limit(n);
    with open(filename, 'w') as file:
        file.write('[')
        for document in cursor:
            file.write(dumps(document))
            file.write(',')
        file.write(']')
    print("json export ok")

def keywords(filename):
    # Returns an array of words from a comma separeted list
    fichier = open(filename, "r")
    listKeywords = fichier.readline()
    listKeywords = listKeywords.split(',')
    fichier.close()
    return listKeywords

def hash(text):
    # Function that takes text, a string, as an argument and returns the sum of it's characters ASCII codes.
    number = 0
    for i in range(len(text)):
        number += ord(text[i])
    return number

def ecritureJSON(id,text,date,author):
    # Function that writes a tweet in a JSON file.

    # Content creation
    obj = {"id":id, "text" : text,"date" : date,  "author": author}
    # Writing in JSON, it'll be created if it doesn't exist.
    with open('data/tweetsAPI.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False))
    f.close()
    
def ecritureCSV(id, text,date,author):
    # Function that writes a tweet in a CSV file.
    # Content creation.
    write = "\n" + id +"," + text + "," + date + "," + author
    # Writing in CSV, it'll be created if it doesn't exist.
    fichier = open("data/tweetsAPI.csv", "a", encoding="utf-8")
    fichier.write(write)
    fichier.close()

def keywordsIN(keywords,chaine):
    # Function that takes chaine ,a string, and keywords ,a list, as an argument and returns True if one
    # of the words in the list is in the sring and False otherwise.
    isIN =False
    for keyword in keywords:
        if (chaine.find(keyword)!= -1):
            isIN = True
            print("from keyword: "+keyword)
    return isIN

def previousDate(day, hour):
    # Function that takes two integers, day and hour, as arguments and returns the ISO8601 normalised date of
    # day days and hour hours before.
    date = datetime.now()
    date = date - timedelta(days=day, hours =hour+2)
    # Convertion to string
    date1 = date.strftime("%Y-%m-%d")
    date2 = date.strftime("%H:%M:%S")
    dateISO8601 = date1 + "T" + date2 + "Z"
    return dateISO8601

def dateAct():
    # Function that returns the ISO8601 normalised actual date.
    dateISO8601 = previousDate(0, 0)
    return dateISO8601

def datePreviousDay():
    # Function that returns the ISO8601 normalised date of the previous day.
    dateISO8601 = previousDate(1, 0)
    return dateISO8601

def updateDate():
    # Save the query date in a file date.txt
    date = dateAct()
    fichier = open("data/date.txt", "w", encoding="utf-8")
    fichier.write(date)
    fichier.close()
    print("Stamp date updated")

def lastDate():
    # Returnd last query date in date.txt
    fichier = open("data/date.txt", "r")
    date = fichier.readline()
    fichier.close()
    return date

def chooseDate():
    print("Choose latest date for tweet collect :")
    print("For yesterday, type : y")
    print("For the last collect date, type : d")
    print("else type the number how many days and hours prior you want it to be, type : days,hours")
    val = input()
    if (val == "y"):
        return datePreviousDay()
    if (val == "d"):
        return lastDate()
    else : 
        val = val.split(',')
        return previousDate(int(val[0]), int(val[1]))

def dbDate(date):
    # Function that takes date, a string, as an argument and returns it's form to put in the database
    # Tweeter format i.e. 2021-07-12T13:28:50.000Z
    date = date[0:4]+date[5:7]+date[8:10]+date[11:13]+date[14:16]+date[17:19]
    return int(date)

def clean(text):
    # Function that take a str text in argument and if it's retweet cut the first word and then return it
    ind = 0
    if (text[0]=='R' and text[1]=='T'):
        while (text[ind] != ':' and ind<len(text)):
            ind = ind + 1
        text = text[ind+1:]
    i = 0
    while(i<len(text)):
        if (text[i]=='@'):
            j=i
            while(j<len(text) and text[j]!=' '):
                j+=1
            text = text[:i]+text[j+1:]
        else:
            i+=1
    return text
 
def check(text):
    text = clean(text)
    checkText = True
    if (keywordsIN(keywords("data/keywords.txt"),text) == False):
        checkText = False
    return checkText    
