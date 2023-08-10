"""Adelaide Metro Display"""

import math
import realtime_gtfs_handler as rt
import static_gtfs_handler as s
import leds

TRAIN_ROUTES = ["BEL", "FLNDRS", "GAW", "GAWC", "GRNG", "NOAR", "OSBORN", "OUTHA", "SALIS", "SEAFRD"]
FIRST_RUN = True

def get_distance(lat_1,long_1,lat_2,long_2):
    """Gets distance between point 1 and point 2"""
    lat_1 = float(lat_1)
    long_1 = float(long_1)
    lat_2 = float(lat_2)
    long_2 = float(long_2)

    return math.dist([lat_1,long_1], [lat_2,long_2])


def old_get_closest_stop(lat, long, route_id, trips, stop_times, stops):

    closest_stop = s.Stop
    closest_dist = 9999
    possible_stops = s.get_stops_on_route(route_id,trips,stop_times,stops)

    for possible_stop in possible_stops:
        stop_lat, stop_long = possible_stop.get_stop_position()

        dist_to_train = get_distance(lat,long,stop_lat,stop_long)

        if dist_to_train < closest_dist:
            closest_stop = possible_stop
            closest_dist = dist_to_train

    return closest_stop

def get_closest_train_stop(train, train_routes):
    closest_distance = 9999

    train_lat, train_long = train.get_vehicle_position()
    route = train.get_route_id()
    stops = train_routes[route]

    for stop in stops:
        stop_lat, stop_long = stop.get_stop_position()
        
        dist = get_distance(train_lat, train_long, stop_lat, stop_long)

        if dist < closest_distance:
            closest_stop = stop
            closest_distance = dist

    return closest_stop

def main():
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


    feed_url = "https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions"

    print("Get GTFS Feed")
    gtfs_feed = rt.get_feed(feed_url)
    print("Get Entities")
    gtfs_entities = rt.get_entities(gtfs_feed)

    print("Get Train Routes")
    train_routes = s.get_stops_by_route(TRAIN_ROUTES, trips, stop_times, stops)

    print("Get List of Trains")
    trains = []
    for entity in gtfs_entities:
        route_id = entity.get_route_id()
        if route_id in TRAIN_ROUTES:
            trains.append(entity)

    stops_with_trains = []
    for train in trains:
        stops_with_trains.append(get_closest_train_stop(train,train_routes))

    for stop in stops_with_trains:
        print(stop.get_stop_name())

if __name__ == "__main__":
    main()