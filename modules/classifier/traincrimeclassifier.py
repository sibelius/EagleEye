#!/usr/bin/env python
'''
 This code train a classifier to identify tweets related to crimes
 It also save the classifier pipeline in the file CrimeClassifier.pickle

@author:        "Sibelius Seraphini"
@contact:       "sseraphini@albany.edu"
@date:          Tue Apr 22 10:56:23 EDT 2014
@version:       "1"
'''

import json
import numpy as np
import pickle # To save the classifier pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from util import StemmedCountVectorizer

def train_classifier():
    ''' Train the crime classifier '''
    filename_tweets = 'data/train_tweets.txt'
    filename_labels = 'data/train_tweets_labels.txt'

    print('Loading tweets and labels...')
    # Load tweets and theirs labels
    tweets = json.load(open(filename_tweets, 'r'))
    y = np.array(json.load(open(filename_labels, 'r')))

    # Extract the text of tweets, and transform to lowercase
    txt = [t['text'].lower() for t in tweets]

    # Generate a Document Term Matrix with 100 features
    # it excludes the stop_words
    stemmed_count_vectorizer = StemmedCountVectorizer(stop_words='english',
            max_features=100)

    # TfIdfTransformer
    tfidf_transformer = TfidfTransformer()

    # A linear SVM classifier
    svm_classifier = LinearSVC()

    # Define the pipeline for the classification
    # 1 - Transform the text for a token count vector
    # 2 - Apply the TfIdf transformation for this vector
    # 3 - Employ the a LinearSVM Classifier
    pipeline = Pipeline([('StemmedCountVectorizer',
        stemmed_count_vectorizer),('TfIdfTransformer',
            tfidf_transformer), ('LinearSVC', svm_classifier)])

    print('Training the classifier...')
    pipeline.fit(txt, y)

    # Save the pipeline
    print('Saving the classifier...')
    pickle.dump(pipeline, open('CrimeClassifier.pickle','w'))

    # Print some statistics of this classifier
    print_stats(pipeline, txt, y)

def print_stats(clf, X, y):
    ''' Calculate the precision, recall, and F1 score for the classifier clf'''
    print('Calculation Precision, Recall and F1-Score...')
    # 5-fold cross validation
    precision = cross_val_score(clf, X, y, cv=5, scoring='precision')
    recall = cross_val_score(clf, X, y, cv=5, scoring='recall')
    f1_score = cross_val_score(clf, X, y, cv=5, scoring='f1')

    print("Precision: %0.2f (+/- %0.2f)" %
            (precision.mean(), precision.std() * 2))
    print("Recall: %0.2f (+/- %0.2f)" % (recall.mean(), recall.std() * 2))
    print("F1 Score: %0.2f (+/- %0.2f)" % (f1_score.mean(), f1_score.std() * 2))

if __name__ == '__main__':
    train_classifier()
