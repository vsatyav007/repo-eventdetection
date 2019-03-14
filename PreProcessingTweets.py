# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 19:59:51 2019

@author: Satya
"""
#remove urls
#remove date & time
#remove latitude & Longitude
#remove HashTags
#Remove Emojis or special characters
#remove @tags

import re
import os
import emoji

def preprocess():
    os.mkdir(os.getcwd()+'/processeddata/')
    processeddir=os.getcwd()+'/processeddata/'
    cwd=os.getcwd()+'/disatersdata/'
    for subdir, dirs, files in os.walk(cwd):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".txt"):
                basefilename=os.path.basename(filepath)
                filenamewithouext=str(os.path.splitext(basefilename)[0])
                #print(os.path.split(basefilename)[0])
                #print(type(os.path.splitext(basefilename)[0]))
                writefilename=filenamewithouext+'_processed.txt'
                #print(writefilename)
                writefilepath=processeddir+writefilename
                #print(writefilepath)
                try:
                    f1 = open(filepath,'r',encoding='utf-8')
                    f2 = open(writefilepath,"w+",encoding='utf-8')
                    for x in f1:
                        x = re.sub(r'https?:\/\/.*,', ',', x)
                        x=re.sub(r'\d{4}-\d{2}-\d{2} +\d{2}:\d{2}:\d{2},', '', x)
                        x=re.sub(r'[0-9]*,','',x)
                        x=re.sub(r'[0-9]*\.[0-9]*,','',x)
                        x=re.sub(r'-[0-9]*\.[0-9]*','',x)
                        x=re.sub(r'[0-9]*\.[0-9]*','',x)
                        x=re.sub(r'@[a-zA-Z0-9]','',x)
                        x=re.sub(r'[#@:-?;&)(!"*%&]','',x)
                        x=re.sub(r'\d','',x)
                        x=re.sub(r'\d','',x)
                        x=re.sub(r'[^0-9A-Za-z]+g','',x)
                        x=emoji.get_emoji_regexp().sub(u'', x)
                        f2.write(x)
                    f1.close()
                    f2.close()
                finally:               
                    f1.close()
                    f2.close()
                
if __name__=='__main__':
        preprocess()