# -*- coding: utf-8 -*-
"""
@author: Satya
"""
import pandas as pd
import numpy as np
import time
import itertools

def jaccard_similarity(im1, im2):
    """
    Computes the Jaccard metric, a measure of set similarity.

    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size. If not boolean, will be converted.

    Returns
    -------
    jaccard : float
        Jaccard metric returned is a float on range [0,1].
        Maximum similarity = 1
        No similarity = 0
    
    Notes
    -----
    The order of inputs for `jaccard` is irrelevant. The result will be
    identical if `im1` and `im2` are switched.

    """
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)
    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")
    
    intersection = np.logical_and(im1, im2)
    union = np.logical_or(im1, im2)
    l=np.divide(intersection.sum(axis=1), union.sum(axis=1))
    return l

def jaccard():
    events=pd.read_csv('events.csv')
    WPMB=pd.read_csv('WordPairMatrizBinarized.csv')
    events1=np.array(events)
    events1=events1.reshape(-1,events1.shape[0])
    events1=np.repeat(events1,repeats=WPMB.shape[0],axis=0)
    WPMB1=WPMB.iloc[:,2:]
    l=WPMB1.values
    j=jaccard_similarity(l,events1)
    jac=pd.DataFrame(j)
    WPMB['jaccard']=jac
    WPMB.to_csv('Jaccard.csv',index=False)


def wordPairMatrixBinarizer():
    WPECM=pd.read_csv('WordPairEventCountMatrix.csv')
    WP=pd.read_csv('wordpairs.csv')    
    k1=list(itertools.permutations(range(2,12), 3))
    k2=list(itertools.permutations(range(12,22), 3))
    k3=list(itertools.permutations(range(22,32), 3))
    columnsval=[]
    k4=[k1,k2,k3]
    events=[]
    i=2 #setting threshold
    j=0
    for k in k4:        
        for x in k:     
            columnsval.append(WPECM.columns.values[x[1]])
            if 'unaffected' in WPECM.columns.values[x[1]]:
                events.append(0)
            else:
                events.append(1)
    WPMB=pd.DataFrame(np.zeros((WPECM.shape[0],2160)),columns=columnsval)
    for k in k4:    
        for x in k:
            pre=x[0]
            cur=x[1]
            nex=x[2]
            curV=WPECM.iloc[:,cur]
            preV=WPECM.iloc[:,pre]
            nexV=WPECM.iloc[:,nex]    
            WPMB.iloc[:,j]=np.where(np.logical_and(((curV-preV)>i),((curV-nexV)>i)) ,1,0)
            j+=1
    WPMB=pd.concat([WP,WPMB],axis=1)
    WPMB.to_csv('WordPairMatrixBinarized.csv',index=False)
    events1=pd.DataFrame(events,columns=['target'])
    events1.to_csv('events.csv',index=False)

def dataformation():
    df=pd.read_csv('Jaccard.csv')
    df1=pd.DataFrame()
    df=df.sort_values(by='jaccard',ascending=False)
    df1['wordpairs']=df[['firstword','secondword']].apply(lambda x:','.join(x.astype(str)),axis=1)
    df2=pd.concat([df1,df.iloc[:,2:]],axis=1)
    df2.to_csv('concatwordpairs.csv',index=False)
    df3=pd.DataFrame()
    df2=df2.sort_values(['jaccard'],ascending=False)
    df3=df2.iloc[:1500,:]
    df2_Transposed=df3.T
    df2_Transposed.iloc[:df2.shape[1]-1,:].to_csv('Transposedjaccard.csv',header=False)
    df5=pd.read_csv('Transposedjaccard.csv')
    events=pd.read_csv('events.csv')
    df6=pd.concat([df5,events],axis=1)
    df6.to_csv('EventDetectionData.csv',index=False)
    
    
if __name__=='__main__':
    start=time.time()
    events=wordPairMatrixBinarizer()
    jaccard()
    dataformation()
    print('time taken is '+str(time.time()-start))