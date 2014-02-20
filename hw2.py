'''
 This code crawls crime related tweets from New York City, implements the manual
 labeling procedure, and computes the API Recall, Quality Precision, and Quality
 Recall

 February 7
 Sibelius Seraphini
'''
from __future__ import division # Used for float division
import twitter, sys, json, operator
import os # python os module, used for check if a file exists
from dateutil.parser import parse
import re # used for regular expression

reload(sys)
sys.setdefaultencoding("utf-8")

# OAuth Settings
consumer_key = '9JKChCx3ePL2m2KLeL98HQ'
consumer_secret = 'rtMbPwidDXXUXEcqlfnb2QiBEeIllH2Hq30dq92Af58'
access_token_key = '2313873457-9S4sFypeD6OVY5IAtx1e7R64h5Po0zFiWM3X0Xp'
access_token_secret = 'HK5ZhGI2FMzjKs2mzx9Mgs6Tq4uYDgzFzI0gOsUevZagh'

output_folder = 'data/'

myApi=twitter.Api(consumer_key=consumer_key, \
        consumer_secret=consumer_secret, \
        access_token_key=access_token_key, \
        access_token_secret=access_token_secret)

"""
fetch all tweets of a single user
"""
def fetch_historical(user):
    data = {}
    max_id = None
    total = 0
    while True:
        statuses = myApi.GetUserTimeline(screen_name=user, count=200, max_id=max_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print >>sys.stderr, "Fetched %d/%d/%d new/old/total." % (
                newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses])-1
    return data.values()

"""
fetch tweets whose id is bigger than specific id
"""
def fetch_today(user):
    data = {}
    max_id = None
    total = 0
    last_id = get_last_id(user)
    while True:
        statuses = myApi.GetUserTimeline(screen_name=user, count=200, max_id=max_id, since_id=last_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print >>sys.stderr, "Fetched %d/%d/%d new/old/total." % (
                newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses])-1
    return data.values()

def get_last_id(user):
    fname = '%s.txt'%user
    fname = os.path.join(output_folder,fname)
    f = open(fname,'r')
    last_line = f.readlines()[-1]
    tweet = json.loads(last_line)
    f.close()
    return tweet['id']


def txtPrint(user,tweets,out_folder):
    for t in tweets:
        t.pdate = parse(t.created_at)
    key = operator.attrgetter('pdate')
    tweets = sorted(tweets, key=key)
    keytweets = [json.loads(str(rawtweet)) for rawtweet in tweets]
    fname = '%s.txt'%user
    fname = os.path.join(out_folder,fname)
    f = open(fname,'a+')
    for tweet in keytweets:
        f.write(json.dumps(tweet) + '\n')
    f.close()

def crawl_users_historical_tweets(list_users, out_folder):
    for user in list_users:
        data = fetch_historical(user)
        txtPrint(user,data,out_folder)

def crawl_most_recent_tweets(list_users, out_folder):
    for user in list_users:
        data = fetch_today(user)
        txtPrint(user,data,out_folder)

# The first step is to query tweets related to crime
def query_tweets_related_crime():
    # Tweets related to crime almost always have the type of crime and the
    # location of the crime
    query = '(arrest OR arson OR assault OR burglary OR robbery OR shooting \
            OR theft OR vandalism OR crime) AND (ave OR avenue OR street \
            OR st OR rd OR road)'
    geo_nyc = ('40.714623', '-74.006605', '20mi') # Geolocalization of New York City
    MAX_ID = None
    tweets = []
    K = 18
    for it in range(K): # Retrieve up to K * 100 tweets
        temp_tweets = [json.loads(str(raw_tweet)) for raw_tweet \
                in myApi.GetSearch(query, geo_nyc, count = 100,
                    max_id = MAX_ID)]#, result_type='recent')]

        tweets = tweets + temp_tweets
        print('Tweets retrieved: %d' % len(tweets))
        if temp_tweets:
            MAX_ID = temp_tweets[-1]['id']

    return tweets

# Compute the number of tweets made by each user
def freq_users(tweets):
    freq = {}
    for tweet in tweets:
        if( tweet['user']['screen_name'] in freq):
            freq[tweet['user']['screen_name']] += 1
        else:
            freq[tweet['user']['screen_name']] = 1

    return freq

# Manual Labelling Procedure
def manual_labelling(user):
    # Check if these user's tweets has already been labelled
    fname = '%s_labels.txt' % user
    fname = os.path.join(output_folder,fname)

    fname_tweets = '%s.txt' % user
    fname_tweets = os.path.join(output_folder, fname_tweets)

    if os.path.isfile(fname) == True:
        #Load labels
        print('Loading labels...')
        labels = json.load(open(fname, 'r'))
    else: # Manual Labelling Procedure
        # Load the tweets of the user
        tweets = []
        with open(fname_tweets) as json_file:
            for line in json_file:
                tweets = tweets + [json.loads(str(line))]

        # This list contains the labels of the tweets
        # 0 - negative tweet, 1 - positive tweet
        labels = [0] * len(tweets)

        # Label one tweet per time
        print('Manual Labelling, press p for a positive tweet and n for a negative tweet')
        for i in range(len(tweets)):
            answer = raw_input(str(i) + '/' + str(len(tweets)) + ' - ' + tweets[i]['text'] + ' :')
            if answer == 'p':
                labels[i] = 1

        # Save the labels to use later
        json.dump(labels, open(fname, 'w'))

    return labels

# Load the tweets of a file
def loadtweets(fname):
    tweets = []
    with open(fname, 'r') as json_file:
        for line in json_file:
            tweets = tweets + [json.loads(str(line))]
    return tweets

# Main function
def main():
#if __name__ == '__main__':
    # Check with the user another retrieve news tweets
    while True:
        another_query = raw_input('Do you want to query new tweets? (y/n): ')
        if another_query == 'y' or another_query == 'n':
            break

    tweets = []
    if another_query == 'y':
        tweets = query_tweets_related_crime()
        tweets_filename = raw_input('File to save the new tweets: ')
        tweets_filename = os.path.join(output_folder, tweets_filename)

        try:
            f = open(tweets_filename, 'w')
            f.write(json.dumps(tweets) + '\n')
            f.close()
        except:
            print 'Data writting exception.'
    else:
        while True:
            tweets_filename = raw_input('File to read the tweets: ')

            if os.path.isfile(tweets_filename) == True:
                tweets = json.load(open(tweets_filename, 'r'))
                break
            else:
                print('File does not exist')
                again = raw_input('Do you want try another file? (y/n): ')
                if again != 'y':
                    return

    freq = freq_users(tweets)
    v = list(freq.values())
    k = list(freq.keys())

    # Sort by number of tweets
    order = sorted(range(len(v)), reverse=True, key=lambda k: v[k])

    # Show the top 5 users that tweets about crime
    print('Top 10 Twitter Users in crime related tweets with number of tweets about crime')

    for i in range(10):
        print i+1, k[order[i]], v[order[i]]

    while True:
        try:
            selection = int(raw_input('1-10 to select a user to calculate the API Recall, Quality Precision, and Quality Recall: '))
            if (selection < 1) or (selection > 10):
                print('Please provide a integer between 1 and 5')
            else:
                break
        except:
            print('Please provide a integer')

    # Select the user selected to crawl the tweets
    user = k[order[selection-1]]
    user_selected = '@' + k[order[selection-1]]
    fname = '%s.txt' % user_selected
    fname = os.path.join(output_folder,fname)

    print('User Selected: %s' % user_selected)

    # Crawl the tweets of the top Twitter user in crime related tweets
#    if os.path.isfile(fname) == True:
#        crawl_most_recent_tweets([user_selected], output_folder)
#    else:
#        crawl_users_historical_tweets([user_selected], output_folder)
#        crawl_most_recent_tweets([user_selected], output_folder)

    if os.path.isfile(fname) == False:
        crawl_users_historical_tweets([user_selected], output_folder)
        crawl_most_recent_tweets([user_selected], output_folder)


    # Manually labelling process
    labels = manual_labelling(user_selected)

    # Calculate API Recall, Quality Precision, and Quality Recall
    # Load user_tweets
    user_tweets = loadtweets(fname)

    # Crawled Tweets via REST API Query
    user_crawled_text = [t['text'].lower() for t in tweets if t['user']['screen_name'] ==
            user] # Crawled tweets of the selected user

    # Total tweets of the user
    user_tweets_text = [t['text'].lower() for t in user_tweets]

    # Compute E_H
    E_H = [labels[idx]
            for t in user_crawled_text # Map idx of crawled_tweets to the whole tweets set of the user
                for idx in range(len(user_tweets_text))
                    if t == user_tweets_text[idx]]
    E = E_H.count(1) # Positive tweets crawled by the REST API Query
    H = E_H.count(0) # Negative tweets crawled by the REST API Query

    # Check the tweets that match the REST API Query
    # We use regular expression to check it
    regex_typecrime = re.compile(r"(\barrest\b|\barson\b|\bassault\b|\bburglary\b|\brobbery\b|\bshooting\b|\btheft\b|\bvandalism\b|\bcrime\b)")
    #regex_typecrime = re.compile("(arrest|arson|assault|burglary|robbery|shooting|theft|vandalism|crime)")
    regex_place = re.compile(r"(\bave\b|\bavenue\b|\bstreet\b|\bst\b|\brd\b|\broad\b)")
    #regex_place = re.compile(r"(ave|avenue|street|st|rd|road)")

    typecrime_match = [i
            for i in range(len(user_tweets_text))
                for m in [regex_typecrime.search(user_tweets_text[i])]
                    if m ]
    place_match = [i
            for i in range(len(user_tweets_text))
                for m in [regex_place.search(user_tweets_text[i])]
                    if m ]

    # Represent the same elements of that the REST API Query
    both_match = list(set(typecrime_match).intersection(set(place_match)))

    F = len([idx for idx in both_match if labels[idx] == 1])
    F = F - E

    I = len([idx for idx in both_match if labels[idx] == 0])
    I = I - H

    G = labels.count(1)
    G = G - F - E

    J = labels.count(0)
    J = J - I - H

    API_Recall = (E+H) / float(E+H+F+I)
    Quality_Precision = E / float(E + H)
    Quality_Recall = E / float(F + G)


    print('E=%d F=%d G=%d H=%d I=%d J=%d' % (E, F, G, H, I, J))
    print('API Recall: %f' % API_Recall)
    print('Quality Precision: %f' % Quality_Precision)
    print('Quality Recall: %f' % Quality_Recall)

if __name__ == '__main__':
    main()
