'''
CCM
The code below is a derivative of Cards:
"Computer-assisted detection and classification of misinformation about climate change" 
by Travis G. Coan, Constantine Boussalis, John Cook, and Mirjam Nanko.
Cards is licensed under the Apache License 2.0
For information on usage and redistribution, see <https://github.com/traviscoan/cards>
'''

# ML CLASSIFIER AND DB UPDATER
# ----------------------------------------------------------------------

import subprocess
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import ml_utils as u
import pickle
from pymongo import MongoClient
import db as d

nTweets = 400 # Limit for the number of collected tweets

# Import model
# ------------------------------------------------------------------------------
# To import CARDS model use : with open('CARDS_Logistic_Classifier.pkl', 'rb') as f:
with open("data/model.pkl", 'rb') as f:
    logit = pickle.load(f)

# Define tools
vectorizer = logit['vectorizer']
clf = logit['clf']
le = logit['label_encoder']
clf_logit = clf

d.dbConnect()

# Import tweets to analyse
# ------------------------------------------------------------------------------
def updateDB():
    docs_new = []
    ids = []

    # uncomment for global
    # tweets = collection.find({})

    db, collection = d.dbConnect()

    # uncomment for n last tweets
    tweets = collection.find().sort("_id",-1).limit(nTweets);

    for tweet in tweets:
        docs_new.append(u.clean(tweet["text"]))
        ids.append(tweet["_id"])

    # print(docs_new)

    # Vectorise the tweets
    # ------------------------------------------------------------------------------
    X_new_tfidf = vectorizer.transform(docs_new)

    # Predict
    # ------------------------------------------------------------------------------
    predicted = clf_logit.predict(X_new_tfidf)

    # Show tweets, categories and some stats
    stats = np.zeros(len(le.classes_))
    for doc, category in zip(docs_new, predicted):
        stats[category]= stats[category]+1
        # shortT = doc[0:40] # clips tweets for print
        # print('{} => {}'.format(shortT, le.classes_[category]))
        
    # Print classes and number of tweets in each class
    print("STATS FOR THE LAST", nTweets, "TWEETS")
    for i in range(len(stats)):
        print(le.classes_[i], ": ", stats[i])
    print("the percentage of uncategorized tweets is ",100* stats[0]/sum(stats)," %")

    # write in db
    # ------------------------------------------------------------------------------
    for id, category in zip(ids, predicted): 
        collection.update_one({"_id":id},{"$set":{"category":le.classes_[category]}})

    print("last", nTweets, "in DB are classified")    
    print("db updated")

if __name__ == "__main__":
    updateDB()
