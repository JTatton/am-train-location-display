#!/usr/bin/python3
from csv import reader
from os import close
from google.transit import gtfs_realtime_pb2
import urllib.request
import math
import leds
#import time
#import random

# Variable Setup
trains = []
stations = []
url = 'https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions' # URL of GTFS Feed

# Class Setup
class Station:
    def __init__(self, name, lat, long, num):
        self.name = name
        self.lat = lat
        self.long = long
        self.num = num

class Train:
    def __init__(self, id, lat, long, dir):
        self.id = id
        self.lat = lat
        self.long = long
        self.dir = dir
    station = Station

def readCSVofStations():
    with open("stops.csv", "r") as readObj:
        stationsRaw = list(reader(readObj))
        for station in stationsRaw:
            stations.append(Station(station[0], station[1], station[2], station[3]))
    
def calcDistance(x1,y1,x2,y2):
    return math.sqrt( (x2-x1) ** 2 + (y2-y1) ** 2 )

def getGTFSFeed():
    serverResponse = urllib.request.urlopen(url)
    gtfsFeed = gtfs_realtime_pb2.FeedMessage()
    gtfsFeed.ParseFromString(serverResponse.read())
    return gtfsFeed

def isTrain(id):
    if len(id) == 4 and (id.startswith("40") or id.startswith("30") or id.startswith("31")):
        return True
    else:
        return False

def isReplBus(id):
    if id == "H1"\
        or id == "G1"\
        or id == "GA2"\
        or id == "GA3"\
        or id == "B1":
        return True
    else:
        return False


def getTrains():
    feed = getGTFSFeed()
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            vehicleID = entity.vehicle.vehicle.id
            routeID = entity.vehicle.trip.route_id
            vehicleLat = entity.vehicle.position.latitude
            vehicleLong = entity.vehicle.position.longitude
            vehicleDir = entity.vehicle.trip.direction_id

            if isTrain(vehicleID) or isReplBus(routeID):
                trains.append(Train(vehicleID, vehicleLat, vehicleLong, vehicleDir))

def linkTrainsToStations():
    for train in trains:
        minDistance = 10.00
        if train:
            for station in stations:
                dist = calcDistance(train.lat, train.long, float(station.lat), float(station.long))
                if dist < minDistance:
                    train.station = station
                    minDistance = dist

def setLights():
    for train in trains:
        if isTrain(train.id):
            if train.dir == 0:
                leds.light(int(train.station.num)-1, 255, 0, 0)
            else:
                leds.light(int(train.station.num)-1, 200, 0, 55)
        else:
            if train.dir == 0:
                leds.light(int(train.station.num)-1, 0, 255, 0)
            else:
                leds.light(int(train.station.num)-1, 0, 200, 55)
        
def clearLights():
    for train in trains:
        leds.clear(int(train.station.num))

readCSVofStations()
getTrains()
linkTrainsToStations()
leds.setupStrip()
setLights()
clearLights()