# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 12:51:39 2019

@author: Satya
"""

import re
#from collections import Counter
import gensim
import heapq
from operator import itemgetter
from multiprocessing import Pool

model = gensim.models.KeyedVectors.load_word2vec_format('../input/embeddings/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin', 
                                                        binary=True)
words = model.index2word

w_rank = {}
for i,word in enumerate(words):
    w_rank[word] = i

WORDS = w_rank

def words(text): return re.findall(r'\w+', text.lower())

def P(word): 
    "Probability of `word`."
    # use inverse of rank as proxy
    # returns 0 if the word isn't in the dictionary
    return - WORDS.get(word, 0)

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def build_vocab(texts):
    sentences = texts.apply(lambda x: x.split()).values
    vocab = {}
    for sentence in sentences:
        for word in sentence:
            try:
                vocab[word] += 1
            except KeyError:
                vocab[word] = 1
    return vocab
f1 = open("F:/satyaprojects/EventDetection/california_fire_unaffected_filtered_hash.txt",'r',encoding='utf-8')
vocab = build_vocab(f1.read())

top_90k_words = dict(heapq.nlargest(90000, vocab.items(), key=itemgetter(1)))

pool = Pool(4)
corrected_words = pool.map(correction,list(top_90k_words.keys()))

for word,corrected_word in zip(top_90k_words,corrected_words):
    if word!=corrected_word:
        print(word,":",corrected_word)