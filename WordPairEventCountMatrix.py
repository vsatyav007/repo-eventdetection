# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 22:17:18 2019

@author: Satya
"""
import os
import numpy as np
import pandas as pd
import time

def GetWordPairEventCountMatrix():
    pdatawd=os.getcwd()+'/processeddata/'
    df=pd.read_csv('wordpairs.csv')
    v = df.values
    for subdir, dirs, files in os.walk(pdatawd):
        if not dirs :
            eventname=str(os.path.basename(subdir))
            k=np.zeros((df.shape[0],1),dtype=int)
            for file in files:
                filepath = subdir + os.sep + file
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
            df[eventname]=df2
            df2.to_csv(eventname+'.csv',index=False)
    df.to_csv('WordPairEventCountmatrix.csv',index=False)
    print(df.shape)
    
if __name__=='__main__':
    start=time.time()
    GetWordPairEventCountMatrix()
    print('time took:%s'%(time.time()-start))    
    