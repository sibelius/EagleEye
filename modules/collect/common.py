# -*- coding: utf-8 -*-
'''
 This file provide common functions and classes for the collection of tweets task

@author:        "Sibelius Seraphini"
@contact:       "sseraphini@albany.edu"
@date:          Tue Apr 22 10:56:23 EDT 2014
@version:       "1"
'''
import twitter

# OAuth Settings
CONSUMER_KEY = '9JKChCx3ePL2m2KLeL98HQ'
CONSUMER_SECRET = 'rtMbPwidDXXUXEcqlfnb2QiBEeIllH2Hq30dq92Af58'
ACCESS_TOKEN_KEY = '2313873457-9S4sFypeD6OVY5IAtx1e7R64h5Po0zFiWM3X0Xp'
ACCESS_TOKEN_SECRET = 'HK5ZhGI2FMzjKs2mzx9Mgs6Tq4uYDgzFzI0gOsUevZagh'

# Twitter Api to retrieve tweets
MYAPI = twitter.Api(consumer_key=CONSUMER_KEY, \
    consumer_secret=CONSUMER_SECRET, \
    access_token_key=ACCESS_TOKEN_KEY, \
    access_token_secret=ACCESS_TOKEN_SECRET)

def get_value(string, key):
    ''' Return the value if the key exist or None otherwise '''
    if key in string:
        return string[key]
    else:
        return None

class Place:
    ''' This class represents a place '''

    places = {} # Map place id to a place object

    def __init__(self,
            id,
            street_address,
            city,
            region,
            country,
            full_name,
            place_type,
            postal_code):

        self.id = id
        self.street_address = street_address
        self.city = city
        self.region = region
        self.country = country
        self.full_name = full_name
        self.place_type = place_type
        self.postal_code = postal_code

        self.tweets = [] # List the tweets in this place

    @staticmethod
    def parse_json(string):
        id = get_value(string, 'id')

        # Save space for the same places
        if id in Place.places:
            return Place.places[id]
        else:
            if 'attributes' in string:
                att = string['attributes']

                street_address = get_value(att, 'street_address')
                city = get_value(att, 'city')
                region = get_value(att, 'region')
                postal_code = get_value(att, 'postal_code')
            else:
                street_address = None
                city = None
                region = None
                postal_code = None

            country = get_value(string, 'country')
            full_name = get_value(string, 'full_name')
            place_type = get_value(string, 'place_type')

            # Create a new place
            place = Place(
                id,
                street_address,
                city,
                region,
                country,
                full_name,
                place_type,
                postal_code)

            # Save the new place in the list of all places
            Place.places[id] = place

            return place

class Tweet:
    ''' This class represents a tweet '''
    def __init__(self,
        created_at,
        text,
        id,
        retweeted,
        place,
        user):

        self.created_at = created_at
        self.text = text
        self.id = id
        self.retweeted = retweeted

        self.place = place # Localization of this tweet
        self.user = user # User that tweeted this tweet

    @staticmethod
    def parse_json(string):
        created_at = get_value(string, 'created_at')
        text = get_value(string, 'text')
        id = get_value(string, 'id')
        retweeted = get_value(string, 'retweeted')

        # Parse place
        if 'place' in string:
            place = Place.parse_json(string['place'])
        else:
            place = None

        # Parse user
        if 'user' in string:
            user = TwitterUser.parse_json(string['user'])
        else:
            user = None

        # Create the tweet
        tweet = Tweet(
            created_at,
            text,
            id,
            retweeted,
            place,
            user)

        # Bind the tweet to the place
        if place != None:
            place.tweets.append(tweet)

        # Bind the tweet to the user
        if user != None:
            user.tweets.append(tweet)

        return tweet

class TwitterUser:
    ''' This class represents a twitter user '''

    twitterusers = {} # Map user id to user object

    def __init__(self,
            created_at,
            profile_image_url,
            description,
            followers_count,
            id,
            geo_enabled,
            location,
            name,
            screen_name,
            statuses_count):

        self.created_at = created_at
        self.profile_image_url = profile_image_url
        self.description = description
        self.followers_count = followers_count
        self.id = id
        self.geo_enabled = geo_enabled
        self.location = location
        self.name = name
        self.screen_name = screen_name
        self.statuses_count =statuses_count

        self.tweets = [] # List of tweets of this user

    @staticmethod
    def parse_json(string):
        id = get_value(string, 'id')

        if id in TwitterUser.twitterusers:
            return TwitterUser.twitterusers[id]
        else:
            created_at = get_value(string, 'created_at')
            profile_image_url = get_value(string, 'profile_image_url')
            description = get_value(string, 'description')
            followers_count = get_value(string, 'followers_count')
            geo_enabled = get_value(string, 'geo_enabled')
            location = get_value(string, 'location')
            name = get_value(string, 'name')
            screen_name = get_value(string, 'screen_name')
            statuses_count = get_value(string, 'statuses_count')

            # Create the new twitter user
            twitter_user = TwitterUser(
                created_at,
                profile_image_url,
                description,
                followers_count,
                id,
                geo_enabled,
                location,
                name,
                screen_name,
                statuses_count)

            # Save in the list of all twitter users
            TwitterUser.twitterusers[id] = twitter_user

            return twitter_user

class Crime:
    ''' This class represents a crime related to one or more tweets '''
    def __init__(self, id, crimetype):
        self.id = id
        self.tweets = [] # List of tweets that represent this crime
        self.crimetype = crimetype

