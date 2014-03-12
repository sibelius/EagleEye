import os # used to check if a file exists
import json
import sys
import numpy as np

reload(sys)
sys.setdefaultencoding("utf-8")

# Load the tweets of a file
def loadtweets(fname):
    tweets = []
    with open(fname, 'r') as json_file:
        for line in json_file:
            tweets = tweets + [json.loads(str(line))]
    return tweets

if __name__ == '__main__':
    tweets_filename = raw_input('Tweets filename: ')
    print('Loading tweets...')

    tweets = np.load(open(tweets_filename, 'r'))
#    tweets = loadtweets(tweets_filename)

    labels_filename = raw_input('Labels filename: ')

    if os.path.isfile(labels_filename) == True:
        labels = json.load(open(labels_filename, 'r'))
    else:
        labels = []

    total = len(tweets)
    already_labelled = len(labels)

    n = 30

    # Label the rest of tweets
    while(total > already_labelled):
        #Label one tweet per time
        print('P - positive tweet\nN - negative tweet\nS - save progress')

        for i in range(n):
            print('(%d:%d:%d)- %s : ' %
                    (already_labelled+i, i, total,tweets[already_labelled+i]))
        ans = raw_input('ans: ')

        if ans == 'p' or ans == 'n':
            if ans == 'p':
                number = int(raw_input('number: '))
            else:
                number = -1

            for i in range(n):
                if i == number:
                    labels.append(1)
                else:
                    labels.append(0)
            already_labelled = already_labelled + n
        elif ans == 's':
            break
    json.dump(labels, open(labels_filename, 'w'))
