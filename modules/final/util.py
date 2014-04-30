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

