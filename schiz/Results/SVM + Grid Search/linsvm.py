
import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn import svm, grid_search


print("Load the training/test data using pandas")
train = pd.read_csv("./Desktop/schiz/concat_train/trainconcat.csv")
test  = pd.read_csv("./Desktop/schiz/concat_test/testconcat.csv")
train_features = train.ix[:,1:411] #train data features
train_label = train["Class"] #train data labels
#test = (test - test.mean()) / (test.max() - test.min())
train_features = (train_features - train_features.mean()) / (train_features.max() - train_features.min())
features = list(train.columns[1:411]) #liste of train features
label = list(train["Class"])
print("Preprocessing data")
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [0.00001, 0.0001, 0.001, 0.01, 0.1,1, 10, 100, 1000,10000]}]
svc = SVC(C=0.000001, class_weight='auto', coef0=0.0, degree=3,kernel="linear",probability=True,random_state=None, shrinking=True, tol=0.000001, verbose=False)
clf = grid_search.GridSearchCV(svc, tuned_parameters)
clf.fit(train_features, label)


scores = cross_validation.cross_val_score(clf,train_features,label,cv=2,scoring='roc_auc')
print(scores)

#def get_score(clf, train_features, train_label):
#    X_train, X_test, y_train, y_test = cross_validation.train_test_split(train_features, train_label, test_size=0.12, random_state=0)
#    clf.fit(X_train, y_train)
#    print clf.score(X_test, y_test) 

print("Training Support Vector Machine")

print("Make predictions on the test set")
test_probs = (clf.predict_proba(test[features])[:,1])
submission = pd.DataFrame({"id": test["Id"], "probability": test_probs})
submission.to_csv("rf_xgboost_submission.csv", index=False)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
