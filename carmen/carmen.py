# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 21:08:47 2013

@author: chen
"""

from hose_util import lookup, get_date1, get_date
from generic_funs import geo_check_tweet    
import re
import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class LocationResolver(object):

    def __init__(self):
        
        self.stateFullNames = []
        self.countryFullNames = []
        self.stateAbbreviationToFullName = dict()
        self.countryAbbreviationToFullName = dict()
        self.geocodeLocationResolver = None
        self.useUnknownPlaces = True        
        self.newLocationIndex = Constants.NEW_LOCATION_STARTING_INDEX
        self.statePattern = ".+,\\s*(\\w+)"
        self.placeNameToNormalizedPlaceName = dict()
        self.idToLocation = dict()
        self.locationNameToLocation = dict()
        self.locationToParent = dict()
        self.locationToChildren = dict()
        self.locationToId = dict()
        
        self.usePlace = CarmenProperties.getBoolean("use_place")
        self.useGeocodes = CarmenProperties.getBoolean("use_geocodes")
        self.useUserString = CarmenProperties.getBoolean("use_user_string")
        self.useUnknownPlaces = CarmenProperties.getBoolean("use_unknown_places")
        
        logger.info("Geocoding using these resources:")
        if self.usePlace:
            logger.info('place')
        if self.useGeocodes:
            logger.info('geocodes')
        if self.useUserString:
            logger.info("user profile")
        
        logger.info("Loading location resources.")
        
        loadLocationFile(CarmenProperties.getString("locations"))
        self.idToLocation[-1] = Location.getNoneLocation()
        knownLocations = []
        for location in self.idToLocation.values():
            knownLocations.append(location)
            
        for location in knownLocations:
            parent = self.createParentOfLocation(location)
            if parent:
                self.locationToParent[location] = parent
            if not self.locationToChildren.has_key(parent):
                self.locationToChildren[parent] = []
            currentLocation = parent
            parent = self.createParentOfLocation(currentLocation)
            while parent:
                if not self.locationToParent.has_key(currentLocation):
                    self.locationToParent[currentLocation] = parent
                if not self.locationToChildren.has_key(parent):
                    self.locationToChildren[parent] = []
                self.locationToChildren[parent].append(currentLocation)

        if self.usePlace:
            loadNameAndAbbreviation(CarmenProperties.getString("place_name_mapping"), None, self.placeNameToNormalizedPlaceName, False)

        loadNameAndAbbreviation(CarmenProperties.getString("state_names_file"), self.stateFullNames, self.stateAbbreviationToFullName, True);
        loadNameAndAbbreviation(CarmenProperties.getString("country_names_file"), self.countryFullNames, self.countryAbbreviationToFullName, True);
        
        if self.useGeocodes:
            self.geocodeLocationResolver = GeocodeLocationResolver()
            for location in self.idToLocation.values():
                self.geocodeLocationResolver.addLocation(location)
        

    def getPlaceFromTweet(tweet):
        if tweet.has_key('place'):
            return tweet['place']
        else:
            return None
    
    def getUserFromTweet(tweet):
        if tweet.has_key('user'):
            return tweet['user']
        else:
            return None
    
    def getLocationFromTweet(tweet):
        user = getUserFromTweet(tweet)
        if user:
            location = lookup(user,'location')
            if location:
                return location
        return None
        
    def getLatLngFromTweet(tweet):
        return geo_check_tweet(tweet)
    
    def loadNameAndAbbreviation(filename, fullName, abbreviations, secondColumnKey):
        for line in open(filename).readlines():
            splitString = line.lower().split('\t')
            splitString[0] = splitString[0].strip()
            if fullName:
                fullName.append(splitString[0])
            if (abbreviations != None):
                if not secondColumnKey:
                    abbreviations[splitString[0]] = splitString[1]
                else:
                    abbreviations[splitString[1]] = splitString[0]
            
    def resolveLocationUsingPlace(tweet):
        place = getPlaceFromTweet(tweet)
        if place == None:
            return None
            
        url = lookup(place, 'url')
        id = lookup(place, 'id')
        country = lookup(place, 'country')
        if country == None:
            logger.warn("Found place with no country: {}".format(place))
            return None
        if placeNameToNormalizedPlaceName.has_key(country.lower):
            country = placeNameToNormalizedPlaceName[country.lower]
            
        placeType = lookup(place, 'place_type')
        if placeType.lower() == 'city':
            city = lookup(place, 'name')
            if country.lower() == 'united states':
                fullName = lookup(place, 'full_name')
                state = None
                if not fullName:
                    logger.warn("Found place with no full_name: {}".format(place))
                    return None
                match = re.search(".+,\\s*(\\w+)", fullName)
                if match:
                    matchedString = match.group().lower()
                    if stateAbbreviationToFullName.has_key(matchedString):
                        state = stateAbbreviationToFullName[matchedString]
                return getLocationForPlace(country, state, None, city, url, id)
            else:
                return getLocationForPlace(country, None, None, city, url, id)
        elif placeType.lower() == 'admin':
            state = lookup(place, 'name')
            return getLocationForPlace(country, state, None, None, url, id)
        elif placeType.lower() == 'country':
            return getLocationForPlace(country, None, None, None, url, id)
        elif placeType.lower() == 'neighborhood' or placeType.lower() == 'poi':
            fullName = lookup(place, 'full_name')
            if not fullName:
                logger.warn("Found place with no full_name: {}".format(place))
                return None
            splitFullName = fullName.split(',')
            city = None
            if len(splitFullName) > 1:
                city = splitFullName[1]
            return getLocationForPlace(country, None, None, city, url, id)
        else:
            logger.warn("Unknown place type: {}".format(placeType))
        
            

            
        
        
        