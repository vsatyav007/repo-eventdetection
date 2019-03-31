# -*- coding: utf-8 -*-
"""
@author: Satya
"""
import pandas as pd
import numpy as np
import time
import numpy as np


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
    WPMB=pd.read_csv('WordPairMatrizBinarized.csv')
    events=np.array([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0])
    events=events.reshape(-1,events.shape[0])
    events=np.repeat(events,repeats=WPMB.shape[0],axis=0)
    WPMB1=WPMB.iloc[:,2:]
    l=WPMB1.values
    j=jaccard_similarity(l,events)
    jac=pd.DataFrame(j)
    WPMB['jaccard']=jac
    WPMB.to_csv('Jaccard.csv',index=False)


def wordPairMatrixBinarizer():
    WPECM=pd.read_csv('WordPairEventCountMatrix.csv')
    WP=pd.read_csv('wordpairs.csv')
    WPMB=pd.DataFrame(np.zeros((WPECM.shape[0],WPECM.shape[1]-2)),columns=WPECM.columns.values[2:])
    for x in WPECM.columns.values[2:]:
        WPMB[x]=np.where(WPECM[x]>=8,1,0)
    WPMB=pd.concat([WP,WPMB],axis=1)
    WPMB.to_csv('WordPairMatrizBinarized.csv',index=False)
    
if __name__=='__main__':
    start=time.time()
    wordPairMatrixBinarizer()
    jaccard()
    print('time taken is '+str(time.time()-start))