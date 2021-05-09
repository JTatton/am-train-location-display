#!/usr/bin/python3
from csv import reader
from os import read
from google.transit import gtfs_realtime_pb2
import urllib.request
import math
import leds
import time
import random

class Train:
    def __init__(self, id, lat, long, dir):
        self.id = id
        self.lat = lat
        self.long = long
        self.dir = dir

class Station:
    def __init__(self, name, lat, long, num):
        self.name = name
        self.lat = lat
        self.long = long
        self.num = num

trains = []
stations = []

def readCSVofStations():
    with open("stops.csv", "r") as readObj:
        stationsRaw = list(reader(readObj))

        for station in stationsRaw:
            stations.append(Station(station[0], station[1], station[2], station[3]))
    

readCSVofStations()
for station in stations:
    print(station.name + " " + station.lat + " " + station.long + " " + station.num)