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

contraction_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", "don't": "do not",
                    "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", 
                    "how's": "how is",  "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have",
                    "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have",
                    "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have", 
                    "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have",
                    "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", 
                    "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as", "this's": "this is","that'd": "that would",
                    "that'd've": "that would have", "that's": "that is", "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", 
                    "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not",
                    "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will",
                    "what'll've": "what will have", "what're": "what are",  "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", 
                    "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", 
                    "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", 
                    "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                    "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have", "you're": "you are", "you've": "you have"}

def _get_contractions(contraction_dict):
    contraction_re = re.compile('(%s)' % '|'.join(contraction_dict.keys()))
    return contraction_dict, contraction_re

contractions, contractions_re = _get_contractions(contraction_dict)

def replace_contractions(text):
    def replace(match):
        return contractions[match.group(0)]
    return contractions_re.sub(replace, text)


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
                        #replace contraction with acutal words
                        print(x)
                        x=replace_contractions(x)
                        print(x)
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