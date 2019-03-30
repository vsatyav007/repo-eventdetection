# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 18:05:39 2019

@author: Satya
"""
import pandas as pd
import numpy as np
import time
def jaccard():
    WPMB=pd.read_csv('WordPairMatrizBinarized.csv')
    WPMB['sum']=WPMB[WPMB.columns.values[2:]].sum(axis=1)
    WPMB['jaccard']=WPMB['sum']/(WPMB.shape[1]-3)
    WPMB.to_csv('jaccard.csv',index=False)


def wordPairMatrixBinarizer():
    WPECM=pd.read_csv('WordPairEventCountMatrix.csv')
    WP=pd.read_csv('wordpairs.csv')
    WPMB=pd.DataFrame(np.zeros((WPECM.shape[0],WPECM.shape[1]-2)),columns=WPECM.columns.values[2:])
    for x in WPECM.columns.values[2:]:
        WPMB[x]=np.where(WPECM[x]>=6,1,0)
    WPMB=pd.concat([WP,WPMB],axis=1)
    WPMB.to_csv('WordPairMatrizBinarized.csv',index=False)
    
if __name__=='__main__':
    start=time.time()
    wordPairMatrixBinarizer()
    jaccard()
    print('time taken is '+str(time.time()-start))