"""
Functions for handling fetching, parsing and dealing with the GTFS Feed
"""
import leds
from csv import reader
from google.transit import gtfs_realtime_pb2
import urllib.request
import math