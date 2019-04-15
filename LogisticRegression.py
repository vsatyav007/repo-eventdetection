# -*- coding: utf-8 -*-
"""
@author: Satya
"""
import numpy as np
import pandas as pd
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,roc_auc_score

df1=pd.read_csv('EventDetectionData.csv')
scores=[]
for i in range(150,200):
    score=[]
    X_train, X_test, y_train, y_test = train_test_split(df1.iloc[:,1:i], df1['target'], test_size=0.3,random_state=69) # 70% training and 30% test

    log=LogisticRegression()

    rfecv = RFECV(estimator=log, step=1, cv=5, scoring='roc_auc')

    X_train_new=rfecv.fit_transform(X_train, y_train)
    X_test_new=rfecv.transform(X_test)
    
    j= rfecv.n_features_

    
    C_range = 10.**np.arange(-5, 1)

    penalty_options = ['l1','l2']

    param_grid = dict(C=C_range,  penalty=penalty_options)

    grid = GridSearchCV(log, param_grid, cv=5, scoring='roc_auc')

    grid.fit(X_train_new, y_train) 
    
    y_train_pred=grid.predict(X_train_new)
    
    y_test_pred=grid.predict(X_test_new)
    
    y_train_pred_prob=grid.predict_proba(X_train_new)
    
    y_test_pred_prob=grid.predict_proba(X_test_new)
    
    Train_Accuracy=accuracy_score(y_train, y_train_pred)
    
    Train_roc=roc_auc_score(y_train, np.max(y_train_pred_prob,axis=1))
    
    Test_Accuracy=accuracy_score(y_test, y_test_pred)
    
    Test_roc =roc_auc_score(y_test, np.max(y_test_pred_prob,axis=1))
    
    score=[i,j,Train_Accuracy,Train_roc,Test_Accuracy,Test_roc]
    
    scores.append(score)

Metrics=pd.DataFrame(scores,columns=['no.of columns','No.of Features Selected','Train_Accuracy','Train_roc','Test_Accuracy','Test_roc'])

Metrics.to_csv('Metrics_LogisticRegression.csv')



