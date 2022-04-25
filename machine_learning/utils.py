'''
CCM
The code below is a derivative of Cards:
"Computer-assisted detection and classification of misinformation about climate change" 
by Travis G. Coan, Constantine Boussalis, John Cook, and Mirjam Nanko.
Cards is licensed under the Apache License 2.0
For information on usage and redistribution, see <https://github.com/traviscoan/cards>
'''

# UTILITIES FOR MACHINE LEARNING
# ----------------------------------------------------------------------

'''A handful of utility functions.'''

import csv
import json
import time


def flatten(list_of_lists):
    '''
    Takes a list of lists and returns the flattned version.

    Args:
        list_of_lists (list): A list of lists to flatten
    
    Returns: 
        list: The flattened list
    '''

    return [item for sublist in list_of_lists for item in sublist]


def read_csv(path, remove_header=False):
    '''
    Takes an absolute path to a CSV file and returns file as
    a Python list.

    Args:
        path (str): Absolute path to CSV file.
        remove_header (bool): Optionally the first line of the CSV.
    
    Returns: 
        list: The CSV file as a list of lists.
    '''

    with open(path, 'r', encoding='utf-8', errors='replace') as csvfile:
        csvreader = csv.reader(csvfile)
        data_ = [row for row in csvreader]
    
    if remove_header:
        data = data_[1:]
    else:
        data = data_
    
    return data


def write_json(path, content):
    '''
    Takes a path and list of dictionaries and writes a pretty, POSIX
    compatiable JSON file.

    Args:
        path (str): Path to file where JSON should be written.
        content (list): List of dictionaries to write.

    Returns:
        None
    '''

    with open(path, 'w') as f:
        json.dump(content, f, indent=4, separators=(',', ': '), sort_keys=True)
        # add trailing newline for POSIX compatibility
        f.write('\n')


def drop_duplicates(seq):
    '''
    Takes a list and drops duplicates in place.

    Args:
        seq (iterable): Iterable
    
    Returns: 
        list: List without duplicates
    '''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def clean(text):
    # Function that take a str text in argument and if it's retweet cut the first word and cut any word starting with @ then return it
    # Cut RT
    ind = 0
    # find RT
    if (text[0]=='R' and text[1]=='T'):
        # find end of RT word
        while (text[ind] != ':' and ind<len(text)):
            ind = ind + 1
        text = text[ind+1:]
    # Cut @
    i = 0
    # find @
    while(i<len(text)):
        if (text[i]=='@'):
            # find end of @ word
            j=i
            while(j<len(text) and text[j]!=' '):
                j+=1
            text = text[:i]+text[j+1:]
        else:
            i+=1
    return text

def convertLabel(label):
    listLabel =["No category","Ice isn't melting","Heading into ice age","Weather is cold","Hiatus in warming","Sea level rise is exaggerated","Extremes aren't increasing","It's natural cycles","No evidence for Greenhouse effect","Sensitivity is low","No species impact","Not a pollutant","Policies are harmful","Policies are ineffective","Clean energy won't work","We need energy","Science is unreliable","Movement is unreliable"]
    listLabelCode =['0_0','1_1','1_2','1_3','1_4','1_6','1_7','2_1','2_3','3_1','3_2','3_3','4_1','4_2','4_4','4_5','5_1','5_2']
    i=0
    while (i<len(listLabelCode)):
        if (label == listLabelCode[i]):
            return listLabel[i]
        i +=1
    print("INCORRECT LABEL !!")
    return "Incorrect label"

def consolePrint(a,b,c,d,e,f,g):
    # Function that takes seven argument, these must be string or convertible to string, 8 characters max. Then it makes a mock-up display based on these arguments, clear the console and print the mock up
    # Convert arguments to string
    toPrint = [str(a),str(b),str(c),str(d),str(e),str(f),str(g)]
    # Make every member of to print 8 characters long
    for i in range (len(toPrint)):
        while (len(toPrint[i])<8):
            toPrint[i] = toPrint[i] +" "
    # Initialise mock-up display
    consPrint = "|        |        |        |        |        |        |        |"
    for i in range(7):
        # Replace one by one the blanks in consPrint by the argument of consolePrint (character by character)
        for j in range(len(toPrint[i])):
            # If the character is a number then replace the blank by this number
            if (toPrint[i][len(toPrint[i])-(j+1)]=="0" or toPrint[i][len(toPrint[i])-(j+1)]=="1" or toPrint[i][len(toPrint[i])-(j+1)]=="2" or toPrint[i][len(toPrint[i])-(j+1)]=="3" or toPrint[i][len(toPrint[i])-(j+1)]=="4" or toPrint[i][len(toPrint[i])-(j+1)]=="5" or toPrint[i][len(toPrint[i])-(j+1)]=="6" or toPrint[i][len(toPrint[i])-(j+1)]=="7" or toPrint[i][len(toPrint[i])-(j+1)]=="8" or toPrint[i][len(toPrint[i])-(j+1)]=="9") :
                consPrint = consPrint[:(i+1)*9-(j+1)]+toPrint[i][len(toPrint[i])-(j+1)]+consPrint[(i+1)*9-(j):]

    # Clear console and display the mock-up
    print("\033[H\033[J")
    print(consPrint)
    time.sleep(0.5)

# ----------------------------------------------------------------------
# Function to manipulate json file

def write_json(list_id, list_date, list_text):
    # Open json file
    file = open("tweets.json", "w")
    # Dump list into json
    list_json = []
    for id, date, text in zip(list_id, list_date, list_text):
        list_json.append((id , (date, text))) 
    jsonStr = json.dumps(list_json)
    file.write(jsonStr)
    # close file
    file.close()

def get_texts_json():
    # Open json file
    file = open("tweets.json", "r")
    # Open json file and store it's data (a list of tweets' text) in a list
    jsonStr = file.read()
    tweets = json.loads(jsonStr)
    list_text = []
    for tweet in tweets :
        list_text.append(tweet[1][1])
    file.close()
    # Return tweets' text list
    return list_text

def get_dates_json():
    # Open json file
    file = open("tweets.json", "r")
    # Open json file and store it's data (a list of tweets' text) in a list
    jsonStr = file.read()
    tweets = json.loads(jsonStr)
    list_date = []
    for tweet in tweets :
        list_date.append(tweet[1][0])
    file.close()
    # Return tweets' text list
    return list_date

def get_ids_json():
    # Open json file
    file = open("tweets.json", "r")
    # Open json file and store it's data (a list of tweets' text) in a list
    jsonStr = file.read()
    tweets = json.loads(jsonStr)
    list_id = []
    for tweet in tweets :
        list_id.append(tweet[0])
    file.close()
    # Return tweets' text list
    return list_id

def update_json(list_categories):
    # get tweets' data
    # Open json file
    file = open("tweets.json", "r")
    # Open json file and store it's data (a list of tweets' text) in a list
    jsonStr = file.read()
    tweets = json.loads(jsonStr)
    list_id = []
    list_date = []
    list_text = []
    for tweet in tweets :
        list_id.append(tweet[0])
        list_date.append(tweet[1][0])
        list_text.append(tweet[0][1])
    file.close()
    # Return tweets' text list
    file = open("tweets.json", "w")
    # Initalise a list of tuples containing a tweet's text and it's category 
    list_tweets = []
    # fill the list with our datas
    for id, date, text, category in zip(list_id, list_date, list_text, list_categories):
        list_tweets.append((id, (date, text , category)))
    # Convert the list of tuples to a dictionary
    list_json = dict(list_tweets)
    # Write the dictionary in a json file
    jsonStr = json.dumps(list_json)
    file.write(jsonStr)
    # Close json file
    file.close()

def get_categories_json():
    # Open json file
    file = open("tweets.json", "r")
    # Open json file and store it's data (a list of tweets' text) in a list
    jsonStr = file.read()
    list_tweets = json.loads(jsonStr)
    list_categories = []
    for id in list_tweets:
        list_categories.append(list_tweets[id][2])
    file.close()
    # Return tweets' text list
    return list_categories

# ----------------------------------------------------------------------
