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

reload(sys)
sys.setdefaultencoding("utf-8")
#global variables
inputDirectory = '../labelled/'
outputDirectory = '../labelled/StreetsAdded/'
#inputFileName = 'Brooklyn_Crime'
inputFileName = 'unbiased'
#inputFileName = 'NYScanner'

outputFileName = 'Test_{0}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d'))
json_data = []


def filterStreetAddress():
    importJsonDaa()
    for jObject in json_data:
        jObject['AddressInText'] = parseText(jObject['text'])
    printText()
    exportFile()

def json_data_clear():
    json_data = []


#import File contents and returns line by line array
def importFileContents(sFileNameDirectory):
    aFileInformation = []
    with open(sFileNameDirectory) as sFile:
        for line in sFile:
           aFileInformation.append(line)

    return aFileInformation

def importJsonDaa():
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
    Do NOT use we are going to use the street names text file . . . which is going to take up a lot of space
    '(Avenue|Ave|Highway|hwy|Place|pl|Road|rd|Route|rte|Street|st|str|parkway|prkwy)(\.?)' # case insensitive
    '(in|on|near|at|@|near|under|over|below|above|rounnd|around|between|behind|across|up|down|opposite|off of|next to|by|against|over|towards)' # prepositions
    '(west|east|norht|south|e|w|s|n)'
    """
#    regex_place = re.compile(r"(Avenue|Ave|Highway|hwy|Place|pl|Road|rd|Route|rte|Street|st|str)(\.?)", re.IGNORECASE)
    lKey = {}
    dReturn = {}
    lPlace = ['avenue', 'ave', 'place', 'pl', 'road', 'rd', 'route', 'rte', 'street', 'st', 'str', 'parkway', 'pkwy', 'plaza', 'plz', 'lane', 'ln', 'plz', 'plaza', 'drive', 'boulevard', 'blvd']
    # removing 'highway', 'hwy',
#    print "Starting code from: {} -> {}".format(__file__, sys._getframe().f_code.co_name)
    lDirection = ['west', 'east', 'north', 'south', 'e', 'w', 's','n']
    lBurroughs = ['Bronx'.lower(), 'Brooklyn'.lower(), 'Manhattan'.lower(), 'Queens'.lower()]
    sReturn = ''
    key = 0
    iPre = 6 # identifies position of first key word
    iPost = 3 #identifies position of more key words
    sBurrough = ''

    # split the json text into an array to identify words and where they are placed
    for word in sText.split():
        dReturn[str(key)] = word
        key += 1

    # iidentfy place with surrounding words
    for place in lPlace:

        for iKey, word in dReturn.iteritems():
            if re.sub(r'[^a-z0-9]','', word.lower()) == place.lower():
                iCnt = int(iKey) - iPre #look back thru text
                iEnd = int(iKey) + iPost # look forward thru text
                while(iCnt < iEnd):
                    if (iCnt >= 0 and iCnt < len(dReturn.values()) and (str(iCnt) not in lKey)):
                        sText = dReturn[str(iCnt)].lower()
                        if (sText.lower() == '&amp;'.lower()):# convert &amp to and
                            sText = 'and'
                        if (iCnt < int(iKey)+1):
                            if (sText.lower() == 'and'.lower()):
                                lKey[str(iCnt)] = sText
                                sReturn += sText+" "
                                iEnd += iPost
                            elif (sText.lower() == 'on'.lower() or sText.lower() == 'at'.lower()):
                                sReturn = ''
                                lKey = {}
                            elif (re.sub(r'[^a-z0-9]','', sText.lower()) in lBurroughs): # identify burrough
                                lKey[str(iCnt)] = sText
                                sReturn = ''
                                sBurrough = re.sub(r'[^a-z0-9]','', sText.lower())
                            elif (re.sub(r'[^a-z0-9]','', sText.lower()) == 'Staten'.lower() or (re.sub(r'[^a-z0-9]','', sText.lower()) == 'Island'.lower \
                            and lKey[str(iCnt-1)].lower() == 'staten'.lower())):
                                lKey[str(iCnt)] = sText
                                sBurrough = 'staten island'
                            else:
                                lKey[str(iCnt)] = sText
                                sReturn += sText+" "
#                        elif (iCnt >= 0 and iCnt < len(dReturn.values()) and str(iCnt) not in lKey):
                        else:
                            if (sText.lower() == 'ny'.lower()):
                                if (len(sBurrough) > 2):
                                    sReturn += sBurrough + " "
                                    sBurrough = ''
                                lKey[str(iCnt)] = sText
                                sReturn += sText
                                iCnt = iEnd +10
                            elif (re.sub(r'[^a-z0-9]','', sText.lower()) in lBurroughs or re.sub(r'[^a-z0-9]','', sText.lower()) in lDirection): # identify burrough
                                lKey[str(iCnt)] = sText
                                sReturn += sText+" "
                    iCnt += 1

    sReturn += sBurrough
    return sReturn



def findStreets(sText):
    """
    After working on this a bit and thinking about the process - the parse text seems like the better way to go . ..
    Special cases:
    route #A or route ## or ##A (# = number, A = letter, i.e. route 9x)
    A-Z (alpha street, i.e. Avenue U)
    Numbered Streets (First...Tenth, and ##rd, ##th, etc)
    Eastern
    """
    dReturn = {}
    sReturn = ''
    lPlace = ['avenue', 'ave', 'highway', 'hwy', 'place', 'pl', 'road', 'rd', 'route', 'rte', 'street', 'st', 'str', 'parkway', 'pkwy']
    key = 0;
    sStreetTextFile = './resource/NYCMainRoads.txt'

    for sPlace in lPlace:
        sRegexPlaceType = "\b"+sPlace+"\b|"
    sRegexStreetPlace = re.compile(r"("+sRegexPlaceType[:-1]+")")

    for word in sText.split():
       dReturn[str(key)] = word
       key += 1

    aStreetNames = importFileContents(sStreetTextFile)
    for streetName in aStreetNames:
       sRegexStreetName = re.compile(r"\b"+streetName+"\b",re.IGNORECASE)

    return sReturn


def printText():
    for jObject in json_data:
        #print "***************************************************************"
       # print 'screen name', jObject['user']['screen_name']
       # print 'id', jObject['id']
       # print 'time', jObject['created_at']
        print 'text:', jObject['text']
        if 'AddressInText' in jObject:
            print 'AddressInText:', jObject['AddressInText']
        print "***************************************************************"

# main function
def main():
    filterStreetAddress()

#""" Keeep this at the bottom of the code """"
if __name__ == '__main__':
    main()
