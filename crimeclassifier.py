'''
 This code train a classifier to identify tweets related to crimes

 Sibelius Seraphini
'''

from __future__ import division # Used for float division
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.cross_validation import cross_val_score
import nltk.stem

english_stemmer = nltk.stem.SnowballStemmer('english')

# This class add the stem operation to the CountVectorizer class
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()

        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

# Load the tweets of a file
def loadtweets(fname):
    tweets = []
    with open(fname, 'r') as json_file:
        for line in json_file:
            tweets = tweets + [json.loads(str(line))]
    return tweets

#tweets = np.array(json.load(open('labelled/total.txt')) + json.load(open('labelled/unbiased.txt')))
#y = np.array(json.load(open('labelled/total_labels.txt')) + json.load(open('labelled/unbiased_labels.txt')))

if __name__ == '__main__':
    filename_tweets = 'labelled/aggregated/train_tweets.txt'
    filename_labels = 'labelled/aggregated/train_tweets_labels.txt'

    # Load tweets and theirs labels
    tweets = json.load(open(filename_tweets, 'r'))
    y = np.array(json.load(open(filename_labels, 'r')))

    # Extract the text of tweets, and transform to lowercase
    txt = [t['text'].lower() for t in tweets]

    # Generate a Document Term Sparse Matrix
#    count_vector = CountVectorizer() #ngram_range=(1,3)
#    count_vector.fit(txt)
#    word_counts = count_vector.transform(txt)

    # Generate a Document Term Sparse Matrix
    vectorizer = StemmedCountVectorizer(stop_words='english', max_features=100) # remove the stop_words
    vectorizer.fit(txt)
    word_counts = vectorizer.transform(txt)

    # Apply the TfIdf transformation to the matrix
    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit(word_counts)
    X = tfidf_transformer.transform(word_counts)

    # Create a Linear SVM Classifier
    clf = LinearSVC()

    # Calculate the precision, recall, and F1 score for our classifier using a
    # 5-fold cross validation
    precision = cross_val_score(clf, X, y, cv=5, scoring='precision')
    recall = cross_val_score(clf, X, y, cv=5, scoring='recall')
    f1_score = cross_val_score(clf, X, y, cv=5, scoring='f1')

    print("Precision: %0.2f (+/- %0.2f)" % (precision.mean(), precision.std() * 2))
    print("Recall: %0.2f (+/- %0.2f)" % (recall.mean(), recall.std() * 2))
    print("F1 Score: %0.2f (+/- %0.2f)" % (f1_score.mean(), f1_score.std() * 2))
