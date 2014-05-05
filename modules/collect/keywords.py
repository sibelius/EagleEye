#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 This file provide function to collect tweets based on keywords

@author:        "Sibelius Seraphini"
@contact:       "sseraphini@albany.edu"
@date:          Tue Apr 22 10:56:23 EDT 2014
@version:       "1"
'''
import common

filename_keywords = 'listofkeywords.txt'

# Load a list of keywords from a file
def loadkeywords()
    # Remove the \n of each line
    keywords = [line.rstrip() for line in open('listofkeywords.txt')]

    return keywords

# Build a OR query using the keywords list
def buildQuery(keywords):
    query = ' OR '.join(keywords)
    return query


