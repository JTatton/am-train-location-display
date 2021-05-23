#!/usr/bin/python3
from csv import reader
from os import close
from google.transit import gtfs_realtime_pb2
import urllib.request
import math
import leds
import time
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
    def __init__(self, id, route, lat, long, dir):
        self.id = id
        self.route = route
        self.lat = lat
        self.long = long
        self.dir = dir
    closeStation = Station

class Colour:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

belair = Colour(42,75,30)
seaford = Colour(100,65,19)
gawler = Colour(76,23,20)
outerharbor = Colour(0,49,77)


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
        or id == "GA1"\
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
                trains.append(Train(vehicleID, routeID, vehicleLat, vehicleLong, vehicleDir))

def linkTrainsToStations():
    for train in trains:
        minDistance = 10.00
        if train:
            for station in stations:
                dist = calcDistance(train.lat, train.long, float(station.lat), float(station.long))
                if dist < minDistance:
                    train.closeStation = station
                    minDistance = dist

def setLights():
    for train in trains:
        print(str(train.route) + " " + str(train.closeStation.name))
        if train.route == "BEL":
            leds.light(int(train.closeStation.num)-1,belair.red, belair.green, belair.blue)
        elif train.route == "OUTHA":
            leds.light(int(train.closeStation.num)-1,outerharbor.red, outerharbor.green, outerharbor.blue)
        elif train.route == "GRNG":
            leds.light(int(train.closeStation.num)-1,outerharbor.red, outerharbor.green, outerharbor.blue)
        elif train.route == "FLNDRS":
            leds.light(int(train.closeStation.num)-1,seaford.red, seaford.green, seaford.blue)
        elif train.route == "SEAFRD":
            leds.light(int(train.closeStation.num)-1,seaford.red, seaford.green, seaford.blue)
        elif train.route == "GA1":
            leds.light(int(train.closeStation.num)-1,gawler.red, gawler.green, gawler.blue)
        elif train.route == "GA2":
            leds.light(int(train.closeStation.num)-1,gawler.red, gawler.green, gawler.blue)
        elif train.route == "GA3":
            leds.light(int(train.closeStation.num)-1,gawler.red, gawler.green, gawler.blue)
        else:
            leds.light(int(train.closeStation.num)-1,255,255,255)
    leds.show()
        
def clearLights():
    for train in trains:
        try:
            leds.clear(int(train.closeStation.num))
        except:
            print("Out of Range")

readCSVofStations()

try:
    while(True):
        getTrains()
        linkTrainsToStations()
        leds.setupStrip()
        clearLights()
        setLights()
        time.sleep(15)
except KeyboardInterrupt:
    leds.clearAll()
    print("Exiting")