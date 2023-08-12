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
import timeit

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
    
    def get_trip_id(self):
        return self.trip_id


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
    """Reads feed_info.txt as CSV into FeedInfo Object"""
    with open("google-transit/feed_info.txt") as file:
        reader = csv.DictReader(file)

        for row in reader:
            return FeedInfo(row)


def read_stop_csv():
    """Reads Stops as CSV to List of Stop Class"""
    stops = []

    with open("google-transit/stops.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stops.append(Stop(row))

    return stops


def read_stop_times_csv():
    """Reads stop_times.txt as CSV and return list of StopTime"""
    stop_times = []

    with open("google-transit/stop_times.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stop_times.append(StopTime(row))

    return stop_times


def read_trips_csv():
    """Reads trips.txt as CSV into list of Trip"""
    trips = []

    with open("google-transit/trips.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            trips.append(Trip(row))

    return trips


def read_routes_csv():
    """Reads routes.txt and returns list of Route"""
    routes = []

    with open("google-transit/routes.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            routes.append(Route(row))

    return routes


def read_agency_csv():
    """Reads agency.txt and returns list of Agency"""
    agencies = []

    with open("google-transit/agency.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            agencies.append(Agency(row))

    return agencies

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


def get_stop_id_on_route(route_id: str, trips: list, stop_times: list) -> list:
    """Returns List of Stop IDs on Route"""
    valid_trip_ids = []
    valid_stop_ids = []

    for trip in trips:
        if trip.get_route_id() == route_id:
            if trip.get_trip_id() not in valid_trip_ids:
                valid_trip_ids.append(trip.get_trip_id())

    for stop_time in stop_times:
        if stop_time.get_trip_id() in valid_trip_ids:
            if stop_time.get_stop_id() not in valid_stop_ids:
                valid_stop_ids.append(stop_time.get_stop_id())
    
    return valid_stop_ids


def get_stops_on_route(route_id: str, trips: list, stop_times: list, stops: list) -> list:
    """Returns List of Stops on Route"""
    valid_trip_ids = []
    valid_stop_ids = []
    valid_stops = []

    for trip in trips:
        if trip.get_route_id() == route_id:
            trip_id = trip.get_trip_id()
            if trip_id not in valid_trip_ids:
                valid_trip_ids.append(trip_id)

    for stop_time in stop_times:
        if stop_time.get_trip_id() in valid_trip_ids:
            stop_id = stop_time.get_stop_id()
            if stop_id not in valid_stop_ids:
                valid_stop_ids.append(stop_id)

    for stop in stops:
        stops_stop_id = stop.get_stop_id()
        if stops_stop_id in valid_stop_ids:
            if stops_stop_id not in valid_stops:
                valid_stops.append(stop)
                
    return valid_stops


def get_stop_position_from_id(stop_id: str, stops: list) -> tuple:
    """Search for stop_id (str) in stops (list of Stop) and return stop_position (lat, long)"""

    for stop in stops:
        if stop.get_stop_id() == stop_id:
            return stop.get_stop_position()
  

def get_stops_from_route_list(routes: list, trips: list, stop_times: list, stops: list) -> dict:
    """Takes list of Routes as strs and returns dict 
    key: route, value: list of Stop"""

    valid_stops = {}

    for route in routes:
        valid_stops[route] = get_stops_on_route(route, trips, stop_times, stops)

    return valid_stops

def main():
    """Main should only call when testing"""
    print("Static GTFS Handler")

    gtfs_zip_url = "https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip"

    #extract_gt_zip(download_gt_zip(gtfs_zip_url))

    #feedinfo = read_feed_info_csv()
    print("Read Stops")
    stops = read_stop_csv()
    print("Read Stop Times")
    stop_times = read_stop_times_csv()
    print("Trips")
    trips = read_trips_csv()
    #routes = read_routes_csv()
    #agency = read_agency_csv()

    route_list = ["BEL", "FLNDRS", "GAW", "GAWC", "GRNG", "NOAR", "OSBORN", "OUTHA", "SALIS", "SEAFRD"]

    stops = get_stops_from_route_list(route_list, trips, stop_times, stops)

    #stops = get_stops_on_route("BEL",trips,stop_times,stops)

    positions = []
    for stop in stops:
        for astop in stops[stop]:
            positions.append(astop.get_stop_position())

    lats = []
    longs = []

    for pos in positions:
        lat = float(pos[0])
        long = float(pos[1])

        if lat not in lats:
            lats.append(lat)
        
        if long not in longs:
            longs.append(long)

    lats.sort()
    longs.sort()

    diff = 9999

    for i in range(len(lats)-1):
        if lats[i+1] - lats[i] < diff:
            diff = lats[i+1] - lats[i]

    print(f"diff: {diff}")

if __name__ == "__main__":
    main()