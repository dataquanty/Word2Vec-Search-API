#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 15:25:23 2018

@author: dataquanty

Class to be called by the flask api and used to retrieve the closest
match from a text query

"""

import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import pickle
from textcleaning import tokenize, normalize


class TextSearch:
    """
    Text search class used to look up the top n closest matches of documents
    
    It takes as input : 
        a trained model from gensim word2vec
        a matrix file with one vector per description 
        a text documents file with the full text descriptions
    
    Documents vectors are calculated by averaging tokens from the input texts ;
    The same is done with the text query ;
    Then the n closest texts vectors can be computed based on the text query, 
    with cosine similarity
    
    """

    def __init__(self, modelfile, docmatrixfile, textfile):
        """
        At init of the class, data is loaded to memory and normalized with
        L2 norm. 
        See the sklearn.preprocessing.Normalizer for more information and 
        inplementations
        
        """
        # load the gensim.word2vec trained model
        self.model = pickle.load(open(modelfile, 'rb'))
        
        # load the matrix representation of texts
        self.docmatrix = np.load(docmatrixfile)
        
        # load the full text descriptions
        self.texts = pd.read_csv(textfile, sep='|').set_index('index')
        self.vectlen = self.docmatrix.shape[1]
        
        # normalize the documents
        self.docmatrix = normalize(self.docmatrix)

    def searchTop(self, query, n):
        """
        Retrieves the n closest match of a query with the input matrix
        The query should be passed as a string and will be tokenized in the 
        same way as the descriptions were tokenized to ensure a similar 
        processing (and appropriate matching)
        
        If a token is not found is the w2v model, it is skipped (prints an 
        exception 'token not in model')
        
        Returns a dictionary with the following keys : 
            {
                "key" : { keys of the returned description },
                "description" : {full descriptions text}
                "score" : { similarity scores [0-1] }
            }
        
        No threshold is applied on the score, so even if the returned matches
        are low (<0.5), the n top results are returned. 
        
        TODO : add threshold and add parameter n_max to get all the
        matches above threshold (n_max for safety )
        
        """
        vect = np.array([0.]*self.vectlen)

        for token in tokenize(query):
            try:
                vect += self.model.wv[token]
            except:
                print(token, ' not in model')
        """
        normalize function takes a 2d matrix as input, so vectors should
        be reshaped - same behavior with sklearn normalize
        """
        vect = normalize(vect.reshape(1, -1))[0]
        
        """
        dot product on normalized vectors is related to cosine similarity
        and works for text similarity
        """
        calc = np.dot(self.docmatrix, vect)
        indmax = np.argsort(calc)[-n:]

        res = self.texts.iloc[indmax]
        res['score'] = calc[indmax]
        return res.to_dict(orient='index')
        
        
