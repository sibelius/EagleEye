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
import re, string   # remove punctuation

OAuth = tweepy.OAuthHandler(util.CONSUMER_KEY, util.CONSUMER_SECRET)
OAuth.set_access_token(util.ACCESS_TOKEN_KEY, util.ACCESS_TOKEN_SECRET)

class EagleEye(tweepy.StreamListener):
    ''' This is the main class of our application '''
    def __init__(self):
        super(EagleEye, self).__init__()

        # Folders and files to save the collected tweets
        self.output_dir = 'data/'
        self.output_all_tweets = self.output_dir + 'all_tweets.json'
        self.output_crime_related = self.output_dir + 'crime_related.json'
        self.output_with_location = self.output_dir + 'with_location.json'

        # Files that contain the trained classifiers
        self.resource_dir = 'resource/'
        self.filename_classifier = self.resource_dir +  'CrimeClassifier.pickle'
        self.filename_typeclassifier = self.resource_dir + 'TypeCrimeClassifier.pickle'
        self.filename_labels_description = self.resource_dir + 'labels_description.txt'
        self.filename_alias_st = self.resource_dir + 'alias.txt'
        self.filename_alias_bigram = self.resource_dir + 'alias_bigram.txt'
        self.filename_roads = self.resource_dir + 'roads.txt'

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

    def on_data(self, raw_data):
        ''' Handle the tweet data '''
        try:
            tweet = json.loads(str(raw_data))

            # Save all tweet collected
            self.save_tweet(tweet, self.output_all_tweets)

            # Transform the tweet's text in lowercase
            text = tweet['text'].lower()

            # Remove punctuation
            text = self.remove_punctuation(text)

            self.count_all = self.count_all + 1

            # Check whether the tweet is a crime related tweet
            if self.clf_crime.predict([text]) == 1:
                # Define the type of crime of this tweet
                type_crime = self.description[self.clf_typecrime([text])]

                # Save the tweets related to crime with theirs respective types
                tweet['type_crime'] = type_crime

                self.save_tweet(tweet, self.output_crime_related)

                self.count_crime_related = self.count_crime_related + 1

                # Apply the alias dictionary to the text
                text_alias = apply_alias(text)

                # Extract the location of the tweet
                street_address = self.extract_street(text)

                if street_address != "":
                    self.count_with_location = self.count_with_location + 1

                    tweet['street_address'] = street_address

                    self.save_tweet(tweet, self.output_with_location)

            #print("All\tCrimeRelated\tLocation")
            if self.count_all % 100 == 0:
                print("%d\t%d\t\t%d" %
                    (self.count_all, self.count_crime_related, self.count_with_location))

        except:
            print 'Data writting exception.'

    def save_tweet(self, tweet, filename):
        ''' save one tweet for a file '''
        with open(filename, 'a') as output:
            output.write(json.dumps(tweet) + '\n')

    def load_dict(self, filename):
        temp = {}

        with open(filename,'r') as f:
            for line in f:
                (key,val) = line.lower().rstrip('\n').split(',')
                temp[key] = val

        return temp

    def load_alias(self):
        ''' load an alias dict '''

        self.alias_st = self.load_dict(self.filename_alias_st)
        self.alias_bigram = self.load_dict(self.filename_alias_bigram)

    def load_roads(self):
        ''' load a list of roads of us '''
        with open(self.filename_roads,'r') as f:
            self.roads = f.read().lower().splitlines()

        # Remove non-unique roads
        self.roads = np.array(list(set(self.roads)))

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
        for key in self.alias_bigram.keys():
            text = text.replace(key, self.alias_bigram[key])

        return text

    def remove_punctuation(self, text):
        regex = re.compile('[%s]' % re.escape(string.punctuation))

        return regex.sub('', text)

    def extract_street(self, text):
        # Transform text to unicode
        text = text.encode('utf-8')

        address = []
        for road in self.roads:
            if ' ' + road + ' ' in text:
                address.append(road)

        # could be one or more street names
        return " ".join(address)

def main():
    ''' This is the main part of our application '''
    while True:
        try:
            eagle_eye = EagleEye()
            stream = tweepy.Stream(OAuth, eagle_eye)
            stream.filter(locations=[-74, 40, -73, 41]) # New York City
        except:
            print 'Exception occur!'

if __name__ == '__main__':
    main()
