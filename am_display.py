"""Adelaide Metro Display"""

import math
import realtime_gtfs_handler as rt
import static_gtfs_handler as s
import leds

TRAIN_ROUTES = ["BEL", "FLNDRS", "GAW", "GAWC", "GRNG", "NOAR", "OSBORN", "OUTHA", "SALIS", "SEAFRD"]

def get_distance(lat_1,long_1,lat_2,long_2):
    lat_1 = float(lat_1)
    long_1 = float(long_1)
    lat_2 = float(lat_2)
    long_2 = float(long_2)

    return math.dist([lat_1,long_1], [lat_2,long_2])

def get_closest_stop_id(lat, long, route_id, trips, stop_times, stops):

    closest_stop_id = 0
    closest_dist = 9999
    possible_stop_ids = s.get_stop_id_on_route(route_id,trips,stop_times)

    for stop_id in possible_stop_ids:
        s_lat, s_long = s.get_stop_position_from_id(stop_id, stops)

        dist = get_distance(lat,long,s_lat,s_long)

        if dist < closest_dist:
            closest_dist = dist
            closest_stop_id = stop_id

    return closest_stop_id

def main():
    gtfs_zip_url = "https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip"

    #extract_gt_zip(download_gt_zip(gtfs_zip_url))

    feedinfo = s.read_feed_info_csv()
    stops = s.read_stop_csv()
    stop_times = s.read_stop_times_csv()
    trips = s.read_trips_csv()
    routes = s.read_routes_csv()
    agency = s.read_agency_csv()

    feed_url = "https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions"

    gtfs_feed = rt.get_feed(feed_url)
    gtfs_entities = rt.get_entities(gtfs_feed)

    trains = []

    for entity in gtfs_entities:
        route_id = entity.get_route_id()
        if route_id in TRAIN_ROUTES:
            trains.append(entity)

    stop_ids_with_train = []

    for train in trains:
        train_lat, train_long = train.get_position()
        train_route_id = train.get_route_id()
        train_stop_id = get_closest_stop_id(train_lat,train_long,train_route_id,trips,stop_times,stops)
        if train_stop_id not in stop_ids_with_train:
            stop_ids_with_train.append(train_stop_id)
    
    stop_ids_with_train.sort()

    print(stop_ids_with_train)

if __name__ == "__main__":
    main()