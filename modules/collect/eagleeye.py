#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 This file provide function to collect tweets based on Stream API

@author:        "Sibelius Seraphini"
@contact:       "sseraphini@albany.edu"
@date:          Tue Apr 22 10:56:23 EDT 2014
@version:       "1"
'''
import common
import tweepy    # twitter api module - python version
import json      # python json module
import os        # python os module, used for creating folders

OAuth = tweepy.OAuthHandler(common.CONSUMER_KEY, common.CONSUMER_SECRET)
OAuth.set_access_token(common.ACCESS_TOKEN_KEY, common.ACCESS_TOKEN_SECRET)

class EagleEye(tweepy.StreamListener):
    ''' This is the main class of our application '''
    def __init__(self):
        super(EagleEye, self).__init__()
        self.output_dir = 'data/'
        self.output_all_tweets = self.output_dir + 'all_tweets.json'
        self.output_crime_related = self.output_dir + 'crime_related.json'
        self.output_with_location = self.output_dir + 'with_location.json'
        self.count = 0

    def on_data(self, raw_data):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        try:
            jdata = json.loads(str(raw_data))
            output = open(self.output_all_tweets, 'a+')
            output.write(json.dumps(jdata) + '\n')
            output.close()

            self.count = self.count + 1

            print(self.count)

        except:
            print 'Data writting exception.'

def main():
    ''' This is the main part of our application '''
    print('Test')
    while True:
        try:
            eagle_eye = EagleEye()
            stream = tweepy.Stream(OAuth, eagle_eye)
            stream.filter(locations=[-74, 40, -73, 41]) # New York City
        except:
            print 'Exception occur!'
    print('Test1')

if __name__ == '__main__':
    main()
