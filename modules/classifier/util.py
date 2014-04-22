'''
A util file that must be included before loading the classifier file

@author:        "Sibelius Seraphini"
@version:       "1"
@maintainer:    "Sibelius Seraphini"
@email:         "sseraphini@albany.edu"
@status:        "Production"
'''

from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.svm import LinearSVC
import nltk.stem

#english_stemmer = nltk.stem.SnowballStemmer('english')

class StemmedCountVectorizer(CountVectorizer):
    ''' This class add the stem operation to the CountVectorizer class'''
    english_stemmer = nltk.stem.SnowballStemmer('english')

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()

        return lambda doc: (self.english_stemmer.stem(w) for w in analyzer(doc))

