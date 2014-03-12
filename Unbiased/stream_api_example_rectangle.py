'''
 This codes crawls the tweets in SanFrancisco area from Twitter.

 Jan 11, 2014
 Po-Ta Chen
'''

import tweepy    # twitter api module - python version
import datetime  # python datetime module
import json      # python json module
import os        # python os module, used for creating folders

consumer_key = '9JKChCx3ePL2m2KLeL98HQ'
consumer_secret = 'rtMbPwidDXXUXEcqlfnb2QiBEeIllH2Hq30dq92Af58'
access_token_key = '2313873457-9S4sFypeD6OVY5IAtx1e7R64h5Po0zFiWM3X0Xp'
access_token_secret = 'HK5ZhGI2FMzjKs2mzx9Mgs6Tq4uYDgzFzI0gOsUevZagh'
output_folder = 'data/{0}' # the fold stores crawl-down data
OAuth = tweepy.OAuthHandler(consumer_key, consumer_secret)
OAuth.set_access_token(access_token_key, access_token_secret)

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

def main():
    while True:
        try:
            sl = StreamListener()
            stream = tweepy.Stream(OAuth, sl)
            stream.filter(locations=[-74,40,-73,41]) # New York City
        except:
            print 'Exception occur!'

if __name__ == '__main__':
    main()



