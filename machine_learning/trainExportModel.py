# TRAINING MODEL AND EXPORT IT ON THE PI ZERO
# ----------------------------------------------------------------------

from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
from utils import read_csv,clean
from random import randint
import pickle

# Get training data 
data = read_csv('dataset-training/training.csv', True)
print(data[:5])

# Encode labels
claims = [row[1] for row in data]
le = preprocessing.LabelEncoder()
y = le.fit_transform(claims)

# print ("claims are", claims)
print("categories are", le.classes_)

# Vectorize datas
text = [row[0] for row in data]
vectorizer = TfidfVectorizer(min_df=3,  max_features=None,
                            strip_accents='unicode',
                            ngram_range=(1, 2), use_idf=1, smooth_idf=1, sublinear_tf=1)
 
X = vectorizer.fit_transform(text)

# print some info
print('X is', X.shape)
keyword=u'climate'
print(keyword+"'s count is", vectorizer.vocabulary_.get(keyword))

# Fit final logistic classifier. Hyperparameters tuned via grid search using
#  10-fold cross-validation
clf_logit = LogisticRegression(C=7.96,
                            solver='lbfgs',
                            multi_class='ovr',
                            max_iter=200,
                            class_weight='balanced')

# Fit final logit model
clf_logit.fit(X, y)

# print some stats about the model
print("classes", clf_logit.classes_)
print("proba",clf_logit.predict_proba(X))
print("predict X",clf_logit.predict(X))
print("len predict X",len(clf_logit.predict(X)))
print("Score", clf_logit.score(X,y))
print('training done!')

# Export model (By encoding it in binary in a pickle file)
model = {'clf': clf_logit, 'vectorizer' : vectorizer, 'label_encoder':le}
model_pickle = open("model.pkl", 'wb')
pickle.dump(model, model_pickle)
model_pickle.close()

print("model exported")
