# -*- coding: utf-8 -*-
"""
@author: Satya
"""
#remove urls
#remove date & time
#remove latitude & Longitude
#Remove Emojis or special characters
#remove @tags

import re
import os
import emoji
import time
import hashlib
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

#import en_core_web_sm
contraction_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", "don't": "do not",
                    "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", 
                    "how's": "how is",  "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have",
                    "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have",
                    "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have", 
                    "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have",
                    "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", 
                    "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as", "this's": "this is","that'd": "that would",
                    "that'd've": "that would have", "that's": "that is", "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", 
                    "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have","today's": "today is","tomorrow's":"tomorrow is", "wasn't": "was not",
                    "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will",
                    "what'll've": "what will have", "what're": "what are",  "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", 
                    "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", 
                    "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", 
                    "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                    "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have", "you're": "you are", "you've": "you have","&amp;":"and","&lt;":"<","&gt;":">","&le;":"=<","&ge;":">="}
stop_words=set(stopwords.words('english'))

def removestopwords(line):
    words=word_tokenize(line)
    wordslist=[]
    for word in words:
            if not word in stop_words:
                wordslist.append(word)
    return ' '.join(wordslist)           

def _get_contractions(contraction_dict):
    contraction_re = re.compile('(%s)' % '|'.join(contraction_dict.keys()))
    return contraction_dict, contraction_re

contractions, contractions_re = _get_contractions(contraction_dict)

def replace_contractions(text):
    def replace(match):
        return contractions[match.group(0)]
    return contractions_re.sub(replace, text)


#def remove_nameentity(text):
#    r1 = str(text)
#    nlp = en_core_web_sm.load()
#    doc = nlp(r1)
#    print([str(word) for word in doc if word.ent_type_ =='PERSON'])
#    lst=' '.join(([str(word) for word in doc if word.ent_type_ !='PERSON']))
#    return lst


lemmatizer = WordNetLemmatizer()

def nltk2wn_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:                    
        return None

def lemmatize_sentence(sentence):
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))    
    wn_tagged = map(lambda x: (x[0], nltk2wn_tag(x[1])), nltk_tagged)

    res_words = []
    for word, tag in wn_tagged:
        if tag is None:                        
            res_words.append(word)
        else:
            res_words.append(lemmatizer.lemmatize(word, tag))

    return ' '.join(res_words)

def removeUnnecessaryWords(x):
    words=x.split()
    for word in words:
            if not len(word)>1:
               words.remove(word) 
    if len(words)>1:
        return ' '.join(words)
    else:
        return ""
def preprocess():    
    processedir=os.getcwd()+'/processeddata/'
    datawd=os.getcwd()+'/disatersdata/'
    #checking if processed directory is present or not.
    if not os.path.exists(processedir):
        os.mkdir(processedir)
    else:
        #if present remove all the files which ends with .txt
        for file in os.scandir(processedir):
            if file.name.endswith(".txt"):
                os.unlink(file.path)
    for subdir, dirs, files in os.walk(datawd):
        #creating same directory structure as in input tweets
        #getting the folder name as in the input
        dirfolder=os.path.join(processedir,subdir[len(datawd):])
        if not os.path.isdir(dirfolder):
            os.mkdir(dirfolder)
        if not dirs:
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".txt"):
                    basefilename=os.path.basename(filepath)
                    filenamewithouext=str(os.path.splitext(basefilename)[0])
                    writefilename= filenamewithouext+'_processed.txt'
                    #writefilename=filenamewithouext+'.txt'
                    writefilepath=dirfolder+'//'+writefilename
                    try:
                        f1 = open(filepath,'r',encoding='utf-8')
                        linestowrite=set()
                        f2 = open(writefilepath,"w+",encoding='utf-8')
                        for x in f1:
                            x=x.lower()
                            x=replace_contractions(x)                            
                            #x=remove_nameentity(x)
                            #remove urls
                            x = re.sub(r'(via:)? +https?:\/\/.*,', ',', x)
                            #remove datetime
                            x=re.sub(r'\d+:?(\d+)?( +)?([ap]m):?( +([ce]dt)?)?',' ',x)
                            #x=re.sub(r'cdt +',' ',x)
                            x=re.sub(r'\d{4}-\d{2}-\d{2} +\d{2}:\d{2}:\d{2},', '', x)
                            #remove temperature
                            x=re.sub(r'\d+\/\d+°?[cf]',' ',x)
                            #remove numbers
                            x=re.sub(r'[0-9]*,?','',x)
                            #remove floating point numbers
                            x=re.sub(r'-?[0-9]*\.[0-9]*,?',' ',x)
                            #remove hashtags and user tags
                            x=re.sub(r'[#@]( +)?[a-zA-Z0-9.,_:]+','',x)
                            #remove special characters
                            x=re.sub(r'[:-?;&)(!"*%_+$~/\[\]]','',x)
                            #remove emoji's
                            x=emoji.get_emoji_regexp().sub(u'', x)
                            #replace contraction with acutal words                            
                            x=removestopwords(x)
                            x=lemmatize_sentence(x)
                            x=re.sub(r'\'s','',x)                            
                            #removing non word characters and extra spaces in sentence
                            x=re.sub(r'[^\w]', ' ', x)
                            x=re.sub(r'[^a-zA-Z0-9]',' ',x)
                            x=re.sub(r' +',' ',x)
                            #removing white space characters
                            x=re.sub(r' +[a-zA-Z] +','',x)
                            x=x.strip()
                            #x=' '.join()
                            x=removeUnnecessaryWords(x)
                            if str(x)!='':
                                #adding new line character
                                x=x+'\n'
                                hashvalue=hashlib.md5(x.encode('utf-8')).hexdigest()
                                if hashvalue not in linestowrite:
                                    f2.write(x)
                                    linestowrite.add(hashvalue)
                        f1.close()
                        f2.close()
                    except Exception as exc: 
                        print(str(exc))
                        f1.close()
                        f2.close()
   
if __name__=='__main__':
    start=time.time()
    preprocess()
    print('time took:%s'%(time.time()-start))