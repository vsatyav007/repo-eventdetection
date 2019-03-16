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
import time
def preprocess():
    processedir=os.getcwd()+'/processeddata/'
    datawd=os.getcwd()+'/disatersdata/'
    if not os.path.exists(processedir):
        os.mkdir(processedir)
    else:
        for file in os.scandir(processedir):
            if file.name.endswith(".txt"):
                os.unlink(file.path)
    for subdir, dirs, files in os.walk(datawd):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".txt"):
                basefilename=os.path.basename(filepath)
                filenamewithouext=str(os.path.splitext(basefilename)[0])
                writefilename=filenamewithouext+'_processed.txt'
                writefilepath=processedir+writefilename
                try:
                    f1 = open(filepath,'r',encoding='utf-8')
                    f2 = open(writefilepath,"w+",encoding='utf-8')
                    for x in f1:
                        #remove urls
                        x = re.sub(r'https?:\/\/.*,', ',', x)
                        #remove datetime
                        x=re.sub(r'\d{4}-\d{2}-\d{2} +\d{2}:\d{2}:\d{2},', '', x)
                        #remove numbers
                        x=re.sub(r'[0-9]*,?','',x)
                        #remove floating point numbers
                        x=re.sub(r'-?[0-9]*\.[0-9]*,?',' ',x)
                        #remove hashtags and user tags
                        x=re.sub(r'[#@][a-zA-Z0-9]* +',' ',x)
                        #remove special characters
                        x=re.sub(r'[:-?;&)(!"*%_+$~/\[\]]','',x)
                        #remove other characters other than alpha numeric
                        x=re.sub(r'[^0-9A-Za-z]+g','',x)
                        #remove emoji's
                        x=emoji.get_emoji_regexp().sub(u'', x)
                        #x=re.sub(r'\d*','',x)
                        #removing non word characters
                        x=re.sub(r'[^\w]', ' ', x)
                        #removing white space characters
                        x=x.strip()
                        #removing additional white spaces in between sentences
                        x=' '.join(x.split())
                        #adding new line character
                        x=x+'\n'
                        f2.write(x)
                    f1.close()
                    f2.close()
                except:               
                    f1.close()
                    f2.close()
    
if __name__=='__main__':
    start=time.time()
    preprocess()
    print('time took:%s'%(time.time()-start))