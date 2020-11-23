#!/usr/bin/python3
from csv import reader
from google.transit import gtfs_realtime_pb2
import urllib.request
import math
import leds
import time
import random

from leds import clearAll

train = []
trains = [[]]
prevTrains = [[]]

def loadStops():
    with open('station-info.csv', 'r') as readObj:
        csvReader = reader(readObj)
        listOfStations = list(csvReader)
    
    return listOfStations

def downloadGTFSFeed():
    serverResponse = urllib.request.urlopen('https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions')
    gtfsFeed = gtfs_realtime_pb2.FeedMessage()
    gtfsFeed.ParseFromString(serverResponse.read())
    return gtfsFeed

def isTrain(id):
    if len(id) == 4:
        if id.startswith("40") or id.startswith("30") or id.startswith("31"):
            return True
    else:
        return False

def isReplacementBus(id):
    if id.startswith("H1")\
        or id.startswith("G1")\
        or id.startswith("GA2")\
        or id.startswith("GA3")\
        or id.startswith("B1"):
        return True
    else:
        return False

def getTrainsWithPositions(gtfsFeed):
    global trains
    global train
    for entity in gtfsFeed.entity:
        if entity.HasField('vehicle'):
            if isTrain(entity.vehicle.vehicle.id) \
                or isReplacementBus(entity.vehicle.vehicle.id):

                train.clear()
                train.append(entity.vehicle.vehicle.id)
                train.append(entity.vehicle.position.latitude)
                train.append(entity.vehicle.position.longitude)

                trains.append(train.copy())

def distance(x1,y1,x2,y2):
    return math.sqrt( (x2-x1) ** 2 + (y2-y1) ** 2 )

def setLights():
    global trains
    global prevTrains
    copyToPrev()
    trains = [[]]
    adelaideMetroFeed = downloadGTFSFeed()
    getTrainsWithPositions(adelaideMetroFeed)
    clearPrevious()
    for train in trains:
            minDistance = 10.00
            if train:
                train.append("NULL")
                train.append(0)
                for station in stations:
                    dist = distance(train[1],train[2], float(station[1]),float(station[2]))
                    if dist < minDistance:
                        train[3] = station[0]
                        train[4] = station[3]
                        minDistance = dist
                print(train[0] + " is at " + train[3])
                leds.light(int(train[4])-1)

def clearPrevious():
    global prevTrains
    for train in prevTrains:
        try:
            leds.clear(int(train[4])-1)
        except:
            print("Out of Range")

def copyToPrev():
    global trains
    global prevTrains
    for train in trains:
        prevTrain = train.copy()
        prevTrains.append(prevTrain)

leds.setupStrip()
stations = loadStops()

try:
    while(True):
       # trains = [[]]
       # adelaideMetroFeed = downloadGTFSFeed()
       # getTrainsWithPositions(adelaideMetroFeed)
       # leds.clearAll()
       # for train in trains:
       #     minDistance = 10.00
       #     if train:
       #         train.append("NULL")
        #        train.append(0)
        #        for station in stations:
        #            dist = distance(train[1],train[2], float(station[1]),float(station[2]))
        #            strDistance = str( dist)
        #            if dist < minDistance:
        #                train[3] = station[0]
        #                train[4] = station[3]
        #                minDistance = dist
        #        print(train[0] + " is at " + train[3])
        #        leds.light(int(train[4])-1)
        setLights()
        leds.show()
        print("")
        time.sleep(20)

except KeyboardInterrupt:
    leds.clearAll()
