import os # used to check if a file exists
import json
import sys

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
    tweets = loadtweets(tweets_filename)

    labels_filename = raw_input('Labels filename: ')

    if os.path.isfile(labels_filename) == True:
        labels = json.load(open(labels_filename, 'r'))
    else:
        labels = []

    total = len(tweets)
    already_labelled = len(labels)

    # Label the rest of tweets
    while(total > already_labelled):
        #Label one tweet per time
        print('P - positive tweet\nN - negative tweet\nS - save progress')

        ans = raw_input('(%d:%d)- %s : ' %
                (already_labelled, total,tweets[already_labelled]['text']))
        if ans == 'p' or ans == 'n':
            labels.append(int(ans == 'p'))
            already_labelled = already_labelled + 1
        elif ans == 's':
            json.dump(labels, open(labels_filename, 'w'))
            break
