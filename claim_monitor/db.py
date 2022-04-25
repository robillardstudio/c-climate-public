'''
CCM
Copyright (c) 2021 Gaëtan Robillard and Jolan Goulin
BSD Simplified License.
For information on usage and redistribution, and for a DISCLAIMER OF ALL
WARRANTIES, see the file, "LICENSE.txt," in this distribution.
'''

# WRITES TWEETS IN DB
# ----------------------------------------------------------------------

from pymongo import MongoClient, collection
import datetime
import pprint
import cl_utils as u

# Connection to the database

def dbConnect():
    # Comment/uncomment below for cloud access
    # !!! Insert your own DB URL below to instantiate your client !!!
    client = MongoClient('YOUROWNLINKTODB')
    db = client['tweet-database']
    collection = db['tweetsdummy']

    # Comment/uncomment below for local acces
    # client = MongoClient('localhost', 27017)
    # db = client["localtweetdb"]  
    # collection = db["tweets"]

    return db, collection

def post(id, author, text, date):
    # Function that takes as argument the id, author, text and date of a tweet and adds it to the database.
    db, collection = dbConnect()
    tweets = collection
    post = {
        "id": id,
        "author": author,
        "text": text,
        "date": u.dbDate(date)}
    # Post in database
    post_id = tweets.insert_one(post).inserted_id
    # Display the tweet
    pprint.pprint(tweets.find_one({"_id": post_id}))
    print("1 found tweet, added to db")


def isTweetInDB(id):
    # Function that takes as argument the id of an tweet and checks if it's in the database, 
    db, collection = dbConnect()
    tweets = collection
    # checks if tweet is in the database.
    if (tweets.find_one({"id": id}) == None):
        return False
    else:
        print("1 found tweet, already in db")
        return True
