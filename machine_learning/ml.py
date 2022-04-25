'''
CCM
The code below is a derivative of Cards:
"Computer-assisted detection and classification of misinformation about climate change" 
by Travis G. Coan, Constantine Boussalis, John Cook, and Mirjam Nanko.
Cards is licensed under the Apache License 2.0
For information on usage and redistribution, see <https://github.com/traviscoan/cards>
An addition was made to export the model to a .pkl file.
'''

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
