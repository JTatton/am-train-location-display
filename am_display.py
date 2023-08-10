"""Adelaide Metro Display"""

import math
import realtime_gtfs_handler as rt
import static_gtfs_handler as s
import leds

def get_distance(lat_1,long_1,lat_2,long_2):
    return math.dist([lat_1,long_1], [lat_2,long_2])

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

    seaford_stop_ids = s.get_stop_id_on_route("SEAFRD",trips,stop_times)
    
    for stop in stops:
        if stop.get_stop_id() in seaford_stop_ids:
            print(stop.get_stop_name())
        

if __name__ == "__main__":
    main()