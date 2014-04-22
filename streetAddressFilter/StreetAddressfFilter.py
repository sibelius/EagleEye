# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 01:48:40 2014

Attempts to locate street address information in the twitter text
Saves to new file

case insenstive /i
Steet|st(.?)
Road|rd(.?)
Avenue|Ave(.?)
Place|Plaza|pl(.?)
Highway|hwy(.?)
Route|rte(.?)
1st|2nd|3rd|##th??

Strategy: import fiile -> create json linked list - > parse text looking for keywords mentioned above -> 
add new attribute to JSON record [autoStreetAddress] -> export modified json list

@author: Harold Austin
"""
from __future__ import division # Used for float division
import twitter, sys, json, operator, datetime, collections
import os # python os module, used for check if a file exists
from dateutil.parser import parse
import re # used for regular expression
from collections import Counter


#global variables
inputDirectory = '../labelled/'
outputDirectory = '../labelled/StreetsAdded/'
inputFileName = 'Brooklyn_Crime'
outputFileName = 'Test_{0}'.format(datetime.datetime.now().strftime('%Y_%m_%d'))
json_data = []
lKey = {}


def filterStreetAddress():
    importFile()
    for jObject in json_data:
        jObject['AddressInText'] = parseText(jObject['text'])
        lKey_clear()
    exportFile()
    printText()
    

def lKey_clear():
    lKey.clear()

def json_data_clear():
    json_data = []

def importFile():
    json_data_clear()
    with open(inputDirectory+inputFileName+'.txt') as sFile:
        for line in sFile:
            json_data.append(json.loads(line))

def exportFile():
    print "Starting code from: {} -> {}".format(__file__, sys._getframe().f_code.co_name)
    sFile = open(outputFileName, 'a+')
    sFile.write(json.dumps(json_data)+ '\n')
    print "Ending code from: {} -> {}".format(__file__, sys._getframe().f_code.co_name)
    
def parseText(sText):
    """ 
    '(Avenue|Ave|Highway|hwy|Place|pl|Road|rd|Route|rte|Street|st|str)(\.?)' # case insensitive
    '(in|on|near|at|@|near|under|over|below|above|rounnd|around|between|behind|across|up|down|opposite|off of|next to|by|against|over|towards)' # prepositions
    """
#    regex_place = re.compile(r"(Avenue|Ave|Highway|hwy|Place|pl|Road|rd|Route|rte|Street|st|str)(\.?)", re.IGNORECASE)
    dReturn = {}    
    lPlace = ['avenue', 'ave', 'highway', 'hwy', 'place', 'pl', 'road', 'rd', 'route', 'rte', 'street', 'st', 'str']    
#    print "Starting code from: {} -> {}".format(__file__, sys._getframe().f_code.co_name)
    sReturn = ''
    key = 0
    for word in sText.split(): # recursion because I'm too tired to care
        dReturn[str(key)] = word
        key += 1
        
    for place in lPlace:
        for iKey, word in dReturn.iteritems():
#            print str(iKey) + ": " + word
            if word.lower() == place.lower():
                iCnt = int(iKey) - 4
                while(iCnt < int(iKey)+3):
#                    print str(iKey) + ": "+ str(iCnt)+ " " + place.lower()
                    if (iCnt >= 0 and iCnt < len(dReturn.values())):
                        lKey[str(iCnt)] = dReturn[str(iCnt)].lower()
                    iCnt += 1
#                lKey[iKey] = place.lower()
                
    #now that we know where the place value(s) is/are - 
    ldirection = ['west', 'east', 'north', 'south']
    
    sReturn = ''
    if (len(lKey) > 0):
        for skey, word in lKey.iteritems():
            print skey +": " + word
            sReturn += str(word)+" "
    
#    print "Ending code from: {} -> {}".format(__file__, sys._getframe().f_code.co_name)
    return sReturn

def printText():
    for jObject in json_data:
        #print "***************************************************************"
       # print 'screen name', jObject['user']['screen_name']
       # print 'id', jObject['id']
       # print 'time', jObject['created_at']        
        print 'text', jObject['text']
        if 'AddressInText' in jObject:
            print 'AddressInText', jObject['AddressInText']
        print "***************************************************************"

# main function
def main():
    filterStreetAddress()

#""" Keeep this at the bottom of the code """"
if __name__ == '__main__':
    main()