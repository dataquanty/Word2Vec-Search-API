#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 16:12:00 2018

@author: dataquanty
"""

from flask import Flask, request, redirect, url_for, flash, jsonify
from textsearch import TextSearch
import json

"""
Flask API that returns the n closest match of a text query

Takes as input a json query in the following format : 
    {
    "0":"search query number one",
    "1":"search query number two",
    "2":"search query number three",
    ...
    }

Returns a json, see below an example query : 
    
    {
        "0":"screw 12mm",
        "1":"WEIL SCREW 14MM",
        "2":"PLASTIC RULER"
    }

And the API response : 
"0": {
    "486254": {
      "PrimaryDI": "5055662908169", 
      "deviceDescription": "WEIL SCREW 15MM", 
      "score": 0.9808971874473267
    }, 
    "486255": {
      "PrimaryDI": "5055662908145", 
      "deviceDescription": "WEIL SCREW 14MM", 
      "score": 0.9832867778975147
    }, 
    "486256": {
      "PrimaryDI": "5055662908107", 
      "deviceDescription": "WEIL SCREW 12MM", 
      "score": 0.9984706088591793
    }, 
    "486271": {
      "PrimaryDI": "5055662907803", 
      "deviceDescription": "SCARF SCREW 14MM", 
      "score": 0.9830988843545456
    }, 
    "486272": {
      "PrimaryDI": "5055662907780", 
      "deviceDescription": "SCARF SCREW 12MM", 
      "score": 0.9991383984663418
    }
  }, 
  "1": {
    "486255": {
      "PrimaryDI": "5055662908145", 
      "deviceDescription": "WEIL SCREW 14MM", 
      "score": 1.0
    }, 
    "486256": {
      "PrimaryDI": "5055662908107", 
      "deviceDescription": "WEIL SCREW 12MM", 
      "score": 0.9837789865449079
    }, 
    "486270": {
      "PrimaryDI": "5055662907827", 
      "deviceDescription": "SCARF SCREW 16MM", 
      "score": 0.9807465993142839
    }, 
    "486271": {
      "PrimaryDI": "5055662907803", 
      "deviceDescription": "SCARF SCREW 14MM", 
      "score": 0.9984709553907667
    }, 
    "486272": {
      "PrimaryDI": "5055662907780", 
      "deviceDescription": "SCARF SCREW 12MM", 
      "score": 0.9833732279886143
    }
  }, 
  "2": {
    "128236": {
      "PrimaryDI": "10887488232799", 
      "deviceDescription": "PLASTIC WORKMAN", 
      "score": 0.9935797830217448
    }, 
    "166500": {
      "PrimaryDI": "10885425323524", 
      "deviceDescription": "PLASTIC RULER", 
      "score": 1.0
    }, 
    "817102": {
      "PrimaryDI": "J011774560000", 
      "deviceDescription": "Dentalastics\u00ae personal plastic ligatures, orange", 
      "score": 0.8884202724654189
    }, 
    "817105": {
      "PrimaryDI": "J011774557000", 
      "deviceDescription": "Dentalastics\u00ae personal plastic ligatures, purple", 
      "score": 0.8872598116029575
    }, 
    "920321": {
      "PrimaryDI": "817573023578", 
      "deviceDescription": "REL-PLASTIC CONDITIONER 10CC", 
      "score": 0.905961617774754
    }
  }
}

"""



app = Flask(__name__)


@app.route('/api/makecalc/', methods=['POST'])
def makecalc():
    """
    Function run at each API call
    
    TODO: add inputs checks and cleaning
    
    """
    jsonfile = request.get_json()
    res = dict()
    for key in jsonfile.keys():
        # TODO: remove prints after debug
        print(key, jsonfile[key])
        res[key] = textSearch.searchTop(jsonfile[key], 5)
        
    return jsonify(res)
    
    # used for debug
    # return jsonify({"uuid":jsonfile['0']})

        

if __name__ == '__main__':
    """
    The TextSearch class instance is loaded at the init of the flask
    API for performance reasons, meaning that all the inputs matrices are 
    stored as in-memory objects
    Then at each call of the API, the searchTop method is called and uses 
    the in-memory matrices to make the proximity calculation
    
    The largest file - document matrix - is 
        (n documents) x (m vect components) 64 bit float
    
    64 bits is not necessary, this can be optimized. 
    
    
    """
    
    with open("params.json", 'r') as stream:
        params = json.load(stream)

    modelfile = params['modelfile']
    docmatrixfile = params['docmatrixfile']
    textfile = params['textfile']
    textSearch = TextSearch(modelfile, docmatrixfile, textfile)
    app.run(debug=True)