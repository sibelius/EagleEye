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
import datetime  # python datetime module
import json      # python json module
import os        # python os module, used for creating folders

OAuth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
OAuth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

output_folder = 'data/{0}'

class StreamListener(tweepy.StreamListener):
     def __init__(self):
         self.daycount = 0
         self.count = 0
         self.total = 0

     def on_data(self, raw_data):
         output_folder_date = output_folder.format(datetime.datetime.now().strftime('%Y_%m_%d'))
         if not os.path.exists(output_folder_date):
             os.makedirs(output_folder_date)
             self.daycount = self.daycount + 1
             self.count = 0

         output_file = output_folder_date+'/nyc.txt'
         try:
             jdata = json.loads(str(raw_data))
             f = open(output_file, 'a+')
             f.write(json.dumps(jdata) + '\n')
             f.close()

             self.count = self.count + 1
             self.total = self.total + 1
             print self.total, self.daycount, self.count
         except:
             print 'Data writting exception.'
'''
def main():
    while True:
        try:
            sl = StreamListener()
            stream = tweepy.Stream(OAuth, sl)
            stream.filter(locations=[-74,40,-73,41]) # New York City
        except:
            print 'Exception occur!'
'''
