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
    - stops.txt
    - transfers.txt         -- TO DO
    - trips.txt             -- TO DO
"""
from io import BytesIO
import zipfile
import csv
import requests

class FeedInfo:
    """FeedInfo Class
        - Stores infomation about the currency of the feed"""
    def __init__(self,feed):
        self.feed_publisher_name = feed["feed_publisher_name"]
        self.feed_publisher_url = feed["feed_publisher_url"]
        self.feed_lang = feed["feed_lang"]
        self.feed_start_date = feed["feed_start_date"]
        self.feed_end_date = feed["feed_end_date"]
        self.feed_version = feed["feed_version"]

    def get_feed_end_date(self):
        return self.feed_end_date

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

class StopTime():
    """Stop Time Class"""
    def __init__(self,stop_time):
        self.trip_id = stop_time["trip_id"]
        self.arrival_time = stop_time["arrival_time"]
        self.departure_time = stop_time["departure_time"]
        self.stop_id = stop_time["stop_id"]
        self.stop_sequence = stop_time["stop_sequence"]
        self.stop_headsign = stop_time["stop_headsign"]
        self.pickup_type = stop_time["pickup_type"]
        self.drop_off_type = stop_time["drop_off_type"]
        self.shape_dist_traveled = stop_time["shape_dist_traveled"]
        self.timepoint = stop_time["timepoint"]

    def get_stop_id(self):
        return self.stop_id

class Trip():
    def __init__(self, trip):
        self.route_id = trip["route_id"]
        self.service_id = trip["service_id"]
        self.trip_id = trip["trip_id"]
        self.trip_headsign = trip["trip_headsign"]
        self.trip_short_name = trip["trip_short_name"]
        self.direction_id = trip["direction_id"]
        self.block_id = trip["block_id"]
        self.shape_id = trip["shape_id"]
        self.wheelchair_accessible = trip["wheelchair_accessible"]

    def get_route_id(self):
        return self.route_id
    
    def get_trip_id(self):
        return self.trip_id

class Route():
    def __init__(self, route):
        self.route_id = route["route_id"]
        self.agency_id = route["agency_id"]
        self.route_short_name = route["route_short_name"]
        self.route_long_name = route["route_long_name"]
        self.route_desc = route["route_desc"]
        self.route_type = route["route_type"]
        self.route_url = route["route_url"]
        self.route_color = route["route_color"]
        self.route_text_color = route["route_text_color"]
        self.RouteGroup = route["RouteGroup"]

    def get_route_id(self):
        return self.route_id
    
    def get_route_color(self):
        return self.route_color
    
    def get_route_colours_int(self):
        r = "0x" + self.route_color[0:2]
        g = "0x" + self.route_color[2:4]
        b = "0x" + self.route_color[4:]

        return (int(r,0),int(g,0),int(b,0))


class Agency():
    def __init__(self, agency):
        self.agency_id = agency["agency_id"]
        self.agency_name = agency["agency_name"]
        self.agency_url = agency["agency_url"]
        self.agency_timezone = agency["agency_timezone"]
        self.agency_lang = agency["agency_lang"]
        self.agency_phone = agency["agency_phone"]
        self.agency_fare_url = agency["agency_fare_url"]

def read_feed_info_csv():
        with open("google-transit/feed_info.txt") as file:
            reader = csv.DictReader(file)

            for row in reader:
                return FeedInfo(row)

def read_stop_csv():
    """Reads Stops to List of Stop Class"""
    stops = []

    with open("google-transit/stops.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stops.append(Stop(row))

    return stops


def read_stop_times_csv():
    stop_times = []

    with open("google-transit/stop_times.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stop_times.append(StopTime(row))

    return stop_times

def read_trips_csv():
    trips = []

    with open("google-transit/trips.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            trips.append(Trip(row))

    return trips

def read_routes_csv():
    routes = []

    with open("google-transit/routes.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            routes.append(Route(row))

    return routes

def read_agency_csv():
    agency = []

    with open("google-transit/agency.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            agency.append(Agency(row))

    return agency

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

    feedinfo = read_feed_info_csv()
    stops = read_stop_csv()
    stop_times = read_stop_times_csv()
    trips = read_trips_csv()
    routes = read_routes_csv()
    agency = read_agency_csv()

    for route in routes:
        print(route.get_route_id(), route.get_route_color() ,route.get_route_colours_int())

if __name__ == "__main__":
    main()