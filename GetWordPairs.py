# -*- coding: utf-8 -*-

"""
@author: Satya
"""

import os
import pandas as pd
import time
import itertools
from nltk.tokenize import word_tokenize

wordpairspath = os.getcwd()+'/globalwordpairs.csv'


def getwordpairs():
    wordpairs_global = []
    pdatawd = os.getcwd()+'/processeddata'
    for subdir, dirs, files in os.walk(pdatawd):
        if not dirs:
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith('.txt'):
                    f1 = open(filepath, 'r', encoding='utf-8')
                    for line in f1:
                        wordslist = []
                        words = set(word_tokenize(line))
                        for word in words:
                            wordslist.append(word)
                        wordpairs = itertools.combinations(wordslist, 2)
                        [wordpairs_global.append(t) for t in wordpairs]
                    f1.close()
    f2 = open(wordpairspath, 'w+', encoding='utf-8')
    f2.write(str(list(set(tuple(sorted(wordpair)) for wordpair in wordpairs_global))))
    print(len(wordpairs_global))
    print(len(set(tuple(sorted(wordpair)) for wordpair in wordpairs_global)))
    f2.close()


def wordpairstodf():
    pairs = open(wordpairspath, 'r').read()
    df = pd.DataFrame(eval(pairs), columns=['firstword', 'secondword'])
    df.to_csv('wordpairs.csv', index=False)


if __name__ == '__main__':
    start = time.time()
    getwordpairs()
    wordpairstodf()
    print('time took:%s' % (time.time()-start))  # 6.4 seconds
