import os # used to check if a file exists
import json
import sys
import numpy as np
import re

reload(sys)
sys.setdefaultencoding("utf-8")

# Load the tweets of a file
def loadtweets(fname):
    tweets = []
    with open(fname, 'r') as json_file:
        for line in json_file:
            tweets = tweets + [json.loads(str(line))]
    return tweets

def printLabels(labels):
    print('Id - Label')
    for i in range(len(labels)):
        print('%d: %s' % (i, labels[i]))

if __name__ == '__main__':
    tweets_filename = raw_input('Tweets filename: ')
    print('Loading tweets...')
    tweets = np.array(json.load(open(tweets_filename)))
    #tweets = loadtweets(tweets_filename)

    labels_filename = re.sub('\.', '_labels.', tweets_filename)
    labels_description_filename = re.sub('\.', '_labels_description.', tweets_filename)

    # Try to load the label file
    if os.path.isfile(labels_filename) == True:
        labels = json.load(open(labels_filename, 'r'))

        if os.path.isfile(labels_description_filename) == True:
            labels_description = json.load(open(labels_description_filename,
                'r'))
        else:
            labels_description = []
    else:
        labels = []
        labels_description = []

    total = len(tweets)
    already_labelled = len(labels)

    # Label the rest of tweets
    while(total > already_labelled):
        #Label one tweet per time
        printLabels(labels_description)
        print('Number of class or n for new class or s to save progress: ')

        ans = raw_input('(%d:%d)- %s : ' %
                (already_labelled, total,tweets[already_labelled]['text']))

        # Create a new class or category
        if ans == 'n':
            class_name = raw_input('Class name: ')
            labels_description.append(class_name)
        elif ans == 's':
            break
        else:
            try:
                ans = int(ans)
                if ans < len(labels_description):
                    labels.append(ans)
                    already_labelled = already_labelled + 1
            except ValueError:
                ans = ''

    json.dump(labels, open(labels_filename, 'w'))
    json.dump(labels_description, open(labels_description_filename, 'w'))
