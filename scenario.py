'''
CCM
Copyright (c) 2021 Gaëtan Robillard and Jolan Goulin
BSD Simplified License.
For information on usage and redistribution, and for a DISCLAIMER OF ALL
WARRANTIES, see the file, "LICENSE.txt," in this distribution.
'''

# SCENARIO
# ----------------------------------------------------------------------
# Creates a list of 32 sub lists of 28 tweets (id, date, text)
# Distributes each sublist to 32 IPs, which are generated automatically
# ----------------------------------------------------------------------

import argparse
import time
from pythonosc import udp_client
from pymongo import MongoClient
import machine_learning.utils as u

loopTime = 1

# Define number of tweets to fetch
nTweets = 896

# Put tweets' text in a list
tweet_text = []
tweet_id = []
tweet_date = []

# Define messages list, 32 times 28 tweets
# format messages_list[message index][sublist id/date/text][element index]
messages_list = []

# Some functions
# ----------------------------------------------------------------------
def list2Message (address, myList):
  for i in range(len(myList)):
    client.send_message(address, myList[i])
    time.sleep(0.15)

# IPs
# ----------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
    help="The port the OSC server is listening on")
args = parser.parse_args()

# Create a list of raspberry pi0 ip
# ----------------------------------------------------------------------
list_ip = []
for i in range(32):
    if (i>=9):
        list_ip.append("192.168.1.1"+ str(i+1))
    else :
        list_ip.append("192.168.1.10"+ str(i+1))

loopValue = 1

# LOOP
# ----------------------------------------------------------------------
while(True):
  print("loop n°", loopValue) 
  
  # Connection to DB (cloud)
  # --------------------------------------------------------------------
  # !!! Insert your own DB URL below to instantiate your client !!!
  dbClient = MongoClient('YOUROWNLINKTODB')
  db = dbClient['tweet-database']
  collection = db['tweetszkm']
  
  # Connect to DB (local)
  # ------------------------------------------------------------------------------
  # client = MongoClient('localhost', 27017)
  # db = client["localtweetdb"]  
  # collection = db["tweets"]
  
  # Fetch tweets
  # --------------------------------------------------------------------
  tweets = collection.find().sort("_id",-1).limit(nTweets);

  for tweet in tweets:
    tweet_text.append(u.clean(tweet["text"]))
    tweet_id.append(tweet["_id"])
    tweet_date.append(tweet["date"])
    
  print("latest tweet:", tweet_text[0])

  # Put tweets in tweet's list and tweet_list in message_list
  for i in range (32):
    tweet_list_text = []
    tweet_list_id = []
    tweet_list_date = []
    for j in range(28):
        tweet_list_text.append(tweet_text[28*i+j])
        tweet_list_id.append(tweet_id[28*i+j])
        tweet_list_date.append(tweet_date[28*i+j])
    messages_list.append([tweet_list_id,tweet_list_date,tweet_list_text])
    
  print("length of main list:", len(messages_list))
  print("length of tweet in sublist:", len(messages_list[0][2]))
  
  # Send messages
  # --------------------------------------------------------------------
  for i in range(len(list_ip)):
    print(i)
    args.ip = list_ip[i]
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    client.send_message("/simple_message","8080808080808080808080808080")
    client.send_message("/flush",True)
    list2Message("/tweet", messages_list[i][2])
    client.send_message("/ml_process",True)
  
  # Clear lists
  # --------------------------------------------------------------------
  messages_list.clear()
  tweet_text.clear()
  tweet_id.clear()
  tweet_date.clear()
  
  # dbClient.close()
  loopValue += 1
  time.sleep(loopTime)
