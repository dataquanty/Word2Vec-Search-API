#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:37:03 2018

"""

import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from collections import defaultdict
from textcleaning import tokenize
import pickle
import json


"""
Script that creates and dumps the word2vec model and the documents matrix

The word2vec training takes a few minutes to train on a intel i7 CPU with
4 workers (over a million documents as input)
Make sure gensim is properly installed to use the fast version. 

Note : a token frequency dictionary is calculated and used to filter out
tokens with low occurence. The word2vec model has got a min_count parameter 
that is also controlling this, tests can be done to check what's the best
approach

Documents vectors are built by averaging token vectors. 


"""

# Read YAML file
with open("params.json", 'r') as stream:
    params = json.load(stream)

gudidfile = params['gudidfile']
modelfile = params['modelfile']
docmatrixfile = params['docmatrixfile']
textfile = params['textfile']


mat = pd.read_csv(gudidfile,
                  sep='|',usecols=['PrimaryDI','deviceDescription'],encoding='utf8')
mat.dropna(inplace=True,how='any')
mat.drop_duplicates(inplace=True)

texts = [tokenize(document) for document in mat['deviceDescription']]


mat['index']=range(len(mat))
mat[['index','PrimaryDI','deviceDescription']].to_csv(textfile,
   sep='|',index=False)


frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 6]
        for text in texts]

model = Word2Vec(texts, size=100, window=5, min_count=7, workers=4)

# word2vec model dumped to a pickle object
with open(modelfile, 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""
Calculation of the documents vectors by iterating over texts
The result is dumped to a binary npy file 
"""
arr_doc = np.zeros((len(texts),100),dtype=float)
for k, t in enumerate(texts):
    vect = np.zeros((100, ), dtype=float)
    i = 0
    for token in t:
        vect += model.wv[token]
        i += 1
    if i > 0:
        vect = vect/i
    
    arr_doc[k]=vect

np.save(docmatrixfile,arr_doc)
