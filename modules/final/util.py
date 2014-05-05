'''
A util file that must be included before loading the classifier file
It also contains the OAuth keys for twitter API

@author:        "Sibelius Seraphini"
@version:       "1"
@maintainer:    "Sibelius Seraphini"
@email:         "sseraphini@albany.edu"
@status:        "Production"
'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
import nltk.stem
import re, string   # remove punctuation
import json


CONSUMER_KEY = '9JKChCx3ePL2m2KLeL98HQ'
CONSUMER_SECRET = 'rtMbPwidDXXUXEcqlfnb2QiBEeIllH2Hq30dq92Af58'
ACCESS_TOKEN_KEY = '2313873457-9S4sFypeD6OVY5IAtx1e7R64h5Po0zFiWM3X0Xp'
ACCESS_TOKEN_SECRET = 'HK5ZhGI2FMzjKs2mzx9Mgs6Tq4uYDgzFzI0gOsUevZagh'

class StemmedCountVectorizer(CountVectorizer):
    ''' This class add the stem operation to the CountVectorizer class'''
    english_stemmer = nltk.stem.SnowballStemmer('english')

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()

        return lambda doc: (self.english_stemmer.stem(w) for w in analyzer(doc))


def loadkeywords(filename):
    ''' Load a list of keywords from a file '''
    # Remove the \n of each line
    keywords = [line.rstrip() for line in open(filename, 'r')]

    return keywords

def build_query(keywords):
    ''' Build a OR query using the keywords list '''
    query = ' OR '.join(keywords)
    return query

def save_tweet(tweet, filename):
    ''' save one tweet for a file '''
    with open(filename, 'a') as output:
        output.write(json.dumps(tweet) + '\n')

def load_dict(filename):
    ''' Load a python dictionary from a file '''
    temp = {}

    with open(filename,'r') as f:
        for line in f:
            (key , val) = line.lower().rstrip('\n').split(',')
            temp[key] = val

    return temp

def remove_punctuation(text):
    ''' Remove punctuation symbols from a text '''
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    return regex.sub('', text)
