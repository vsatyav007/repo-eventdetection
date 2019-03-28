# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 23:25:28 2019

@author: Satya
"""
import multiprocessing
import os
import pandas as pd
import time
import numpy as np

pdatawd=os.getcwd()+'/processeddata/'
subdirs = [os.path.join(pdatawd, o) for o in os.listdir(pdatawd) if os.path.isdir(os.path.join(pdatawd,o))]
subdirsnames = [o for o in os.listdir(pdatawd) if os.path.isdir(os.path.join(pdatawd,o))]    
df=pd.read_csv('wordpairs.csv')
v=df.values
df1=[]

def GetWordPairEventCountMatrix(pdatawd):
    k=np.zeros((df.shape[0],1),dtype=int)
    for filename in os.listdir(pdatawd):
        eventname=str(os.path.basename(pdatawd))                
        filepath = pdatawd + os.sep + filename
        if filepath.endswith('.txt'):
            f1=open(filepath,'r',encoding='utf-8')
            for line in f1:
                line=line.strip()
                words=line.split()
                for i in range(df.shape[0]):
                    if ((v[i,0] in words) and (v[i,1] in words)):
                        k[i,0]=k[i,0]+1
            f1.close()
    df2=pd.DataFrame({eventname:k[:,0]})
    df2.to_csv(eventname+'pool.csv',index=False)

def appendresults():
    df3=pd.read_csv('wordpairs.csv')
    for name in subdirsnames:
        filename=os.getcwd()+os.sep+name+'pool.csv'
        df4=pd.read_csv(filename)
        df3=pd.concat([df3,df4],axis=1)
    df3.to_csv('WordPairEventCountmatrix.csv',index=False)    
    print(df3.shape)    
           
if __name__=='__main__':
    start=time.time()
    pool=multiprocessing.Pool(processes=len(subdirs))
    for i in range(len(subdirs)):
        pool.apply_async(GetWordPairEventCountMatrix,args=(subdirs[i],))
    pool.close()
    pool.join()
    appendresults()
    print('time took:%s'%(time.time()-start))