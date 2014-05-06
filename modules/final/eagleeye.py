#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 This file provide function to collect tweets based on Stream API

@author:        "Sibelius Seraphini"
@contact:       "sseraphini@albany.edu"
@date:          Tue Apr 22 10:56:23 EDT 2014
@version:       "1"
'''
import util         # OAuth keys and classifier required class
import tweepy       # twitter api module - python version
import json         # python json module
import os           # python os module, used for creating folders
import pickle       # load the trained classifiers
import numpy as np

OAuth = tweepy.OAuthHandler(util.CONSUMER_KEY, util.CONSUMER_SECRET)
OAuth.set_access_token(util.ACCESS_TOKEN_KEY, util.ACCESS_TOKEN_SECRET)

class EagleEye:
    ''' This class process the tweets '''
    def __init__(self):
        # Folders and files to save the collected tweets
        self.output_dir = 'data/'
        self.output_all_tweets = self.output_dir + 'all_tweets.json'
        self.output_crime_related = self.output_dir + 'crime_related.json'
        self.output_with_location = self.output_dir + 'with_location.json'

        # Files that contain the trained classifiers
        self.resource_dir = 'resource/'
        self.filename_classifier = self.resource_dir +  'CrimeClassifier.pickle'
        self.filename_typeclassifier = \
            self.resource_dir + 'TypeCrimeClassifier.pickle'
        self.filename_labels_description = \
            self.resource_dir + 'labels_description.txt'
        self.filename_alias_st = self.resource_dir + 'alias.txt'
        self.filename_alias_bigram = self.resource_dir + 'alias_bigram.txt'
        self.filename_roads = self.resource_dir + 'roads.txt'
        self.filename_states = self.resource_dir + 'states_acronym.txt'

        # Count all tweets
        self.count_all = 0
        self.count_crime_related = 0
        self.count_with_location = 0

        # Create the data folder
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Load classifiers
        self.clf_crime = pickle.load(open(self.filename_classifier, 'r'))
        self.clf_typecrime = pickle.load(open(self.filename_typeclassifier,'r'))

        # Load labels description
        self.description = json.load(open(self.filename_labels_description,'r'))

        # Alias used to improve the street address filtering
        self.alias_st = {}
        self.alias_bigram = {}

        # Load the alias names
        self.load_alias()

        # List of all roads in USA
        self.roads = None

        # Load road names
        self.load_roads()

        # List of all states acronym in USA
        self.states = None

        self.load_states()

    def process_tweet(self, tweet):
        ''' Process one tweet '''
        # Save all tweet collected
        util.save_tweet(tweet, self.output_all_tweets)

        # Transform the tweet's text in lowercase
        text = tweet['text'].lower()

        # Remove punctuation
        text = util.remove_punctuation(text)

        self.count_all = self.count_all + 1

        # Check whether the tweet is a crime related tweet
        if self.clf_crime.predict([text]) == 1:
            # Define the type of crime of this tweet
            type_crime = self.description[self.clf_typecrime.predict([text])]

            # Save the tweets related to crime with theirs respective types
            tweet['type_crime'] = type_crime

            util.save_tweet(tweet, self.output_crime_related)

            self.count_crime_related = self.count_crime_related + 1

            # Apply the alias dictionary to the text
            text = self.apply_alias(text)

            # Extract full address
            street_address = self.extract_full_address(text)

            # Extract the location of the tweet
#            street_address = self.extract_street(text)

            if street_address != "":
                self.count_with_location = self.count_with_location + 1

                tweet['street_address'] = street_address

                # Extract the state information
#                tweet['state'] = self.extract_state(text)

                util.save_tweet(tweet, self.output_with_location)

        #print("All\tCrimeRelated\tLocation")
        if self.count_all % 20 == 0:
            print("%d\t%d\t\t%d" % \
                    (self.count_all, self.count_crime_related, \
                    self.count_with_location))

    def load_alias(self):
        ''' load an alias dict '''

        self.alias_st = util.load_dict(self.filename_alias_st)
        self.alias_bigram = util.load_dict(self.filename_alias_bigram)

    def load_roads(self):
        ''' load a list of roads of us '''
        with open(self.filename_roads,'r') as f_roads:
            self.roads = f_roads.read().lower().splitlines()

        # Remove non-unique roads
        self.roads = np.array(list(set(self.roads)))

    def load_states(self):
        ''' load a list of all states of us '''
        self.states = open(self.filename_states, \
                'r').read().lower().splitlines()

    def apply_alias(self, text):
        ''' apply the alias dict to a text '''

        # First start with the bigram search
        text = self.apply_alias_bigram(text)

        temp = []
        for token in text.split():
            if token in self.alias_st:
                temp.append(self.alias_st[token])
            else:
                temp.append(token)

        return ' '.join(temp)

    def apply_alias_bigram(self, text):
        ''' apply an alias based on bigrams '''
        for key in self.alias_bigram.keys():
            text = text.replace(key, self.alias_bigram[key])

        return text

    def extract_street(self, text):
        ''' extract a street information from a text '''
        # Transform text to unicode
        text = text.encode('utf-8')

        address = []
        for road in self.roads:
            if ' ' + road + ' ' in text:
                address.append(road)

        # could be one or more street names
        return ' '.join(address)

    def extract_state(self, text):
        ''' extract state information from a text '''
        text = text.encode('utf-8')

        for state in self.states:
            if ' ' + state + ' ' in text:
                return state

        return ''

    def extract_full_address(self, text):
        text = text.encode('utf-8')

        address = []
        for road in self.roads:
            if ' ' + road + ' ' in text:
                address.append(road)

        if len(address) == 0:
            return ''

        current_state = None
        for state in self.states:
            if ' ' + state + ' ' in text:
                current_state = state
                break

        begin_address = len(text)+1
        for addr in address:
            if text.find(addr) < begin_address:
                begin_address = text.find(addr)

        if current_state != None:
            end_address = text.find(current_state) + 2
        else:
            end_address = 0
            for addr in address:
                if text.find(addr)+len(addr) > end_address:
                    end_address = text.find(addr)+len(addr)

        return text[begin_address:end_address]

class StreamListener(tweepy.StreamListener):
    ''' This class listen to new tweets '''
    def __init__(self):
        super(StreamListener, self).__init__()

        # The eagleEye class process the tweets
        self.eagle_eye = EagleEye()

    def on_data(self, raw_data):
        ''' Handle the tweet data '''
        try:
            tweet = json.loads(str(raw_data))
            self.eagle_eye.process_tweet(tweet)

        except:
            print 'Data writting exception.'

def main():
    ''' This is our main function '''
    filename_keywords = 'resource/listofkeywords.txt'
    keywords = util.loadkeywords(filename_keywords)

    ''' This is the main part of our application '''
    while True:
        try:
            stream_listener = StreamListener()
            stream = tweepy.Stream(OAuth, stream_listener)
            # Receive tweets from New York city and related to crimes
            stream.filter(locations=[-74, 40, -73, 41], \
                    track = keywords)
        except:
            print 'Exception occur!'

if __name__ == '__main__':
    main()
