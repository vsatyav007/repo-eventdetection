# -*- coding: utf-8 -*-
"""
@author: Satya
"""

import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.metrics import roc_auc_score

df1=pd.read_csv('EventDetectionData.csv')

X_train, X_test, y_train, y_test = train_test_split(df1.iloc[:,1:], df1['target'], test_size=0.3,random_state=69) # 70% training and 30% test

scores=[]

for i in range(150,200):
    model1 = GaussianNB()
    
    model1.fit(X_train.iloc[:,:i], y_train)
    
    y_train_pred1=model1.predict(X_train.iloc[:,:i])
    
    y_test_pred1=model1.predict(X_test.iloc[:,:i])
    
    y_train_pred_prob1=model1.predict_proba(X_train.iloc[:,:i])
    
    y_test_pred_prob1=model1.predict_proba(X_test.iloc[:,:i])
    
    Train_Accuracy=metrics.accuracy_score(y_train, y_train_pred1)
    
    Train_roc=roc_auc_score(y_train, np.max(y_train_pred_prob1,axis=1))
    
    Test_Accuracy=metrics.accuracy_score(y_test, y_test_pred1)
    
    Test_roc =roc_auc_score(y_test, np.max(y_test_pred_prob1,axis=1))
    
    score=[i,Train_Accuracy,Train_roc,Test_Accuracy,Test_roc]
    
    scores.append(score)

Metrics=pd.DataFrame(scores,columns=['no.of columns','Train_Accuracy','Train_roc','Test_Accuracy','Test_roc'])

Metrics.to_csv('Metrics_NaiveBayes.csv')