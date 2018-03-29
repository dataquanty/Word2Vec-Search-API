#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 15:14:57 2018

@author: dataquanty
"""

import re
import numpy as np



def tokenize(document):
    rempat = "[^a-zA-Z0-9,.; -]"
    lstout =  list(filter(None, re.split(r'([0-9]+\.[0-9]+[a-zA-Z]{0,2})|\W+', 
                         re.sub(rempat, ' ', document.lower()))))
    return lstout


def normalize(arr):
    arr = np.array(arr,dtype=float,copy=False)
    for i in range(arr.shape[0]):
        s = np.sum(np.square(arr[i]))
        if s > 0:
            arr[i]=arr[i]/np.sqrt(s)
    return arr