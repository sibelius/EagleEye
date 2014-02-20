from __future__ import division # Division is default float
import numpy as np
import operator
import re

# Return a list with n-grams
def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

def tfidf(collection, ngram):
    # Number of documents in the collection
    N = collection.size

    # Genereate the ngram for each document
    collection_ngram = np.array([find_ngrams(doc.split(), ngram) for doc in
        collection])

    # Array with all the ngrams for all documents
    ngrams_words = np.array(reduce(operator.add, collection_ngram))

    # Transform each ngram in a tuple
    ngrams_tuples = [tuple(row) for row in ngrams_words]

    # Terms represent the unique ngrams
    terms = np.unique(ngrams_tuples)

    # Count the frequency of the ngrams
    tf = np.array([ngrams_tuples.count(tuple(term)) for term in terms])

    # Normalize the Term Frequency
    tf = tf / np.max(tf)

    # Compute the document frequency
    # Problem - this part of the algorithm is very slow
    df = np.zeros(terms.shape[0])
    for i in range(terms.shape[0]):
        try:
#            df[i] = max(1, sum([1 for t in txt if re.search('(\\b' + terms[i] + '\\b)', t)]))
#            df[i] = max(1, sum([((doc == terms[i]).all(1).nonzero())[0].size for doc
#                in collection_ngram]))
            df[i] = max(1, sum([1 for doc in collection_ngram if ((doc ==
                terms[i]).all(1).nonzero())[0].size > 0]))
        except:
            df[i] = (1)

    # TF-IDf = tf * log (N / df)
    tfidf = tf * (1.0 + np.log(float(N) / df))

    return terms, tfidf

# This function work only with single words
def simple(collection):
    N = collection.size

    # Generate a list with all the words in the tweets
    words = reduce(operator.add, [doc.split() for doc in collection])

    # The terms represent only the unique words
    terms = np.array(list(set(words)))

    # Count the frequency of the words
    tf = np.array([words.count(term) for term in terms])

    # Normalize the Term Frequency
    tf = tf / np.max(tf)

    # Compute the document frequency
    df = np.zeros((terms.size))
    for i in range(terms.size):
        try:
            df[i] = max(1, sum([1 for t in txt if re.search('(\\b' + terms[i] + '\\b)', t)]))
        except:
            df[i] = (1)

    # TF-IDf = tf * log2 (N / df)
    tfidf = tf * (1.0 + np.log(float(N) / df))

    print('Total %.03f sec.' % total.interval)

    return terms, tfidf







if __name__ == '__main__':

    # tweets - collection of tweets
    txt = [t['text'] for t in tweets] # Extract the text of the tweets

    N = len(txt) # Number of tweets

    # Generate a list with all the words in the tweets
    words = reduce(operator.add, [t.split() for t in txt])

    # The terms represent only the unique words
    terms = np.array(list(set(words)))

    # Count the frequency of the words
    tf = np.array([words.count(term) for term in terms])

    # Normalize the Term Frequency
    tf = tf / np.max(tf)

    # Compute the document frequency
    df = np.zeros((terms.size))
    for i in range(terms.size):
        try:
            df[i] = max(1, sum([1 for t in txt if re.search('(\\b' + terms[i] + '\\b)', t)]))
        except:
            df[i] = (1)

    # TF-IDf = tf * log2 (N / df)
    tfidf = tf * (1.0 + np.log(float(N) / df))


    # Preprocess
    # Remove numbers


