"""Adelaide Metro Display"""

import math
import realtime_gtfs_handler as rt
import static_gtfs_handler as s
import leds
import csv
from datetime import datetime

#TRAIN_ROUTES = ["BEL", "FLNDRS", "GAW", "GAWC", "GRNG", "NOAR", "OSBORN", "OUTHA", "SALIS", "SEAFRD"]
TRAIN_ROUTES = ["GAW","OUTHA","BEL","SEAFRD"]
UPDATE_DELAY = 25
STOP_THRESHOLD = 4.5e-6

def get_distance(lat_1,long_1,lat_2,long_2):
    """Gets distance between point 1 and point 2"""
    lat_1 = float(lat_1)
    long_1 = float(long_1)
    lat_2 = float(lat_2)
    long_2 = float(long_2)

    return math.dist([lat_1,long_1], [lat_2,long_2])

def get_closest_train_stop(train, train_routes):
    closest_distance = 9999

    train_lat, train_long = train.get_vehicle_position()
    route = train.get_route_id()
    stops = train_routes[route]

    for stop in stops:
        stop_lat, stop_long = stop.get_stop_position()
        
        dist = get_distance(train_lat, train_long, stop_lat, stop_long)

        # Smallest distance between any 2 stops is 5.1e-6
        # We can adjust this threshold
        if dist <= STOP_THRESHOLD:
            print(f"dist <= {STOP_THRESHOLD}")
            closest_stop = stop
            return closest_stop
        elif dist < closest_distance:
            closest_stop = stop
            closest_distance = dist

    return closest_stop

def setup_static_gtfs():
    """Call first for setting up Static GTFS"""
    
    gtfs_zip_url = "https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip"
    #extract_gt_zip(download_gt_zip(gtfs_zip_url))

    #feedinfo = s.read_feed_info_csv()
    #routes = s.read_routes_csv()
    #agency = s.read_agency_csv()
    print("Read Stop CSV")
    stops = s.read_stop_csv()

    print("Read Stop Times CSV")
    stop_times = s.read_stop_times_csv()

    print("Read Trips CSV")
    trips = s.read_trips_csv()

    return (stops, stop_times, trips)

def update_realtime_gtfs():
    """Updates realtime GTFS data """
    feed_url = "https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions"

    print("Get GTFS Feed")
    gtfs_feed = rt.get_feed(feed_url)
    print("Get Entities")
    gtfs_entities = rt.get_entities(gtfs_feed)

    return gtfs_entities

def update(train_stops,stop_led_map):
    print("Update RT GTFS Feed")
    gtfs_entities = update_realtime_gtfs()

    print("Get List of Trains")
    trains = []
    for entity in gtfs_entities:
        route_id = entity.get_route_id()
        if route_id in TRAIN_ROUTES:
            trains.append(entity)

    print("Get Stops with Trains")
    stops_with_trains = []
    for train in trains:
        stops_with_trains.append(get_closest_train_stop(train,train_stops))

    print("Light LEDs")
    leds.clear_all()
    for stop in stops_with_trains:
        leds.light(stop_led_map[stop.get_stop_id()],255,0,0)
        print(stop.get_stop_name())

    leds.show()
    return datetime.now()

def setup_led_strip():
    """Sets up LED stop for Use - runs small test"""
    print("Setting up LED Strip")
    leds.setup_strip()
    leds.clear_all()


def main():
    """Called when running stand-alone"""
    last_update = datetime.now()

    setup_led_strip()
    
    (stops, stop_times, trips) = setup_static_gtfs()

    print("Get Train Routes")
    train_stops = s.get_stops_from_route_list(TRAIN_ROUTES, trips, stop_times, stops)

    stop_led_map = {}
    with open("led_map") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stop_led_map[row["stop_id"]] = int(row["led_num"])
    
    while True:
        try:
            if (datetime.now() - last_update).seconds > UPDATE_DELAY:
                print("\nUpdating")
                print(datetime.now())
                last_update = update(train_stops,stop_led_map)
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            leds.clear_all()
            break

if __name__ == "__main__":
    main()