"""
Module for handling Static GTFS Feed Data

Downloads and Extracts Zip
Imports txts as CSVs for:
    - agency.txt            -- TO DO
    - calendar_dates.txt    -- TO DO
    - calendar.txt          -- TO DO
    - feed_info.txt         -- TO DO
    - Release Notes.txt     -- TO DO
    - routes.txt            -- TO DO
    - shapes.txt            -- TO DO
    - stop_times.txt        -- TO DO
    - stops.txt             -- TO DO
    - transfers.txt         -- TO DO
    - trips.txt             -- TO DO
"""
from io import BytesIO
import zipfile
import csv
import requests

class Stop:
    """Stop class"""
    def __init__(self,stop):
        self.stop_id = stop["stop_id"]
        self.stop_code = stop["stop_code"]
        self.stop_name = stop["stop_name"]
        self.stop_desc = stop["stop_desc"]
        self.stop_lat = stop["stop_lat"]
        self.stop_lon = stop["stop_lon"]
        self.zone_id = stop["zone_id"]
        self.stop_url = stop["stop_url"]
        self.location_type = stop["location_type"]
        self.parent_station = stop["parent_station"]
        self.stop_timezone = stop["stop_timezone"]
        self.wheelchair_boarding = stop["wheelchair_boarding"]

    def get_stop_id(self):
        return self.stop_id
    
    def get_stop_code(self):
        return self.stop_code

    def get_stop_name(self):
        return self.stop_name
    
    def get_stop_position(self):
        return (self.stop_lat,self.stop_lon)
    
    def get_stop(self):
        return (self.stop_id, self.stop_code, self.stop_name, self.stop_desc, self.stop_lat, self.stop_lon, self.zone_id, self.stop_url, self.location_type, self.parent_station, self.stop_timezone, self.wheelchair_boarding)
    

def read_stop_csv():
    """Reads Stops to List of Stop Class"""
    stops = []

    with open("google-transit/stops.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stops.append(Stop(row))

    return stops

def download_gt_zip(url):
    """Downloads google-transit zip and returns request object"""
    if check_gt_url(url):
        try:
            req = requests.get(url)
        except:
            print("Request Error")
            return -1
        else:
            return req


def extract_gt_zip(req):
    """Extracts Zip File to ./google-transit"""
    try:
        file = zipfile.ZipFile(BytesIO(req.content))
    except:
        print("Not a Zip File")
        return -1
    else:
        file.extractall("./google-transit")


def check_gt_url(url):
    """Primitively checks that the url is a google_transit zip"""
    return url.split("/")[-1] == "google_transit.zip"


def main():
    """Main should only call when testing"""
    print("Static GTFS Handler")

    gtfs_zip_url = "https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip"

    #extract_gt_zip(download_gt_zip(gtfs_zip_url))

    stops = read_stop_csv()

    for stop in stops:
        print(f"ID: {stop.get_stop_id()}, Code: {stop.get_stop_code()}, Name: {stop.get_stop_name()}, Lat: {stop.get_stop_position()[0]}, Long: {stop.get_stop_position()[1]}")

if __name__ == "__main__":
    main()