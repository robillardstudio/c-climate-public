# MACHINE LEARNING ON THE PI ZERO
# ----------------------------------------------------------------------

from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import utils as u
import pickle

# Import model
# ------------------------------------------------------------------------------
with open("model.pkl", 'rb') as f:
    logit = pickle.load(f)

# Define tools
vectorizer = logit['vectorizer']
clf = logit['clf']
le = logit['label_encoder']
clf_logit = clf

# ----------------------------------------------------------------------
docs_new = []
ids = []
dates = []
    
def ml_logistic(docs_new):
    # Vectorise the tweets
    # ------------------------------------------------------------------
    X_new_tfidf = vectorizer.transform(docs_new)

    # Predict
    # ------------------------------------------------------------------
    predicted = clf_logit.predict(X_new_tfidf)
    return predicted