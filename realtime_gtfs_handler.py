"""
Module for handling Realtime GTFS Feeds

Joshua Tatton 2023

Currently only working for Adelaide Metro Feed
"""
from urllib.request import urlopen
from google.transit import gtfs_realtime_pb2

class EntityVehicle:
    """Vehicle in Entity"""
    def __init__(self, entity):
        self.vehicle_timestamp = entity.vehicle.timestamp

        self.vehicle_trip = {}
        self.vehicle_trip["trip_id"] = entity.vehicle.trip.trip_id
        self.vehicle_trip["route_id"] = entity.vehicle.trip.route_id
        self.vehicle_trip["direction_id"] = entity.vehicle.trip.direction_id
        self.vehicle_trip["start_date"] = entity.vehicle.trip.start_date
        self.vehicle_trip["schedule_relationship"] = entity.vehicle.trip.schedule_relationship

        self.vehicle_vehicle = {}
        self.vehicle_vehicle["id"] = entity.vehicle.vehicle.id
        self.vehicle_vehicle["label"] = entity.vehicle.vehicle.label

        self.vehicle_position = {}
        self.vehicle_position["latitude"] = entity.vehicle.position.latitude
        self.vehicle_position["longitude"] = entity.vehicle.position.longitude
        self.vehicle_position["bearing"] = entity.vehicle.position.bearing
        self.vehicle_position["speed"] = entity.vehicle.position.speed

    def set_timestamp(self, timestamp):
        """Setter Function for Timestamp"""
        self.vehicle_timestamp = timestamp

    def set_trip(self, trip_id, route_id, direction_id, start_date, schedule_relationship):
        """Setter Function for Trip"""
        self.vehicle_trip["trip_id"] = trip_id
        self.vehicle_trip["route_id"] = route_id
        self.vehicle_trip["direction_id"] = direction_id
        self.vehicle_trip["start_date"] = start_date
        self.vehicle_trip["schedule_relationship"] = schedule_relationship

    def get_timestamp(self):
        """Getter Function returns Timestamp"""
        return self.vehicle_timestamp

    def get_tripid(self):
        """Getter Function returns Trip ID"""
        return self.vehicle_trip["trip_id"]

    def get_routeid(self):
        """Getter Function returns Route ID"""
        return self.vehicle_trip["route_id"]

    def get_vehicleid(self):
        """Getter Function returns Vehicle ID"""
        return self.vehicle_vehicle["id"]

    def get_position(self):
        """Getter Function returns Tuple (latitude, longitude)"""
        return (self.vehicle_position["latitude"], self.vehicle_position["longitude"])

def main():
    """Main should only be called during testing"""
    print("Welcome to GTFSHandler.py")

    feed_url = "https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions"

    print(f"Feed URL: {feed_url}")
    print("Getting Feed")
    gtfs_feed = get_feed(feed_url)

    entities = []

    for entity in gtfs_feed.entity:
        entities.append(EntityVehicle(entity))

    for i in entities:
        print(f"Route ID: {i.get_routeid()}, Vehicle ID: {i.get_vehicleid()}, Lat: {i.get_position()[0]}, Long: {i.get_position()[1]}")

def get_feed(feed_url):
    """Function to get GTFS Feed and Parse to List"""
    server_response = urlopen(feed_url)
    gtfs_feed = gtfs_realtime_pb2.FeedMessage()
    gtfs_feed.ParseFromString(server_response.read())
    return gtfs_feed

if __name__ == "__main__":
    main()
