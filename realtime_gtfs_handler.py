"""
Module for handling Realtime GTFS Feeds

Joshua Tatton 2023

Currently only working for Adelaide Metro Feed
"""
import requests
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

    def get_timestamp(self):
        """Getter Function returns Timestamp"""
        return self.vehicle_timestamp

    def get_trip_id(self):
        """Getter Function returns Trip ID"""
        return self.vehicle_trip["trip_id"]

    def get_route_id(self):
        """Getter Function returns Route ID"""
        return self.vehicle_trip["route_id"]

    def get_vehicle_id(self):
        """Getter Function returns Vehicle ID"""
        return self.vehicle_vehicle["id"]

    def get_vehicle_position(self):
        """Getter Function returns Tuple (latitude, longitude)"""
        return (self.vehicle_position["latitude"], self.vehicle_position["longitude"])


def get_entities(feed):
    """Gets entities from feed and returns list of EntityVehicle"""
    entities = []

    for entity in feed.entity:
        entities.append(EntityVehicle(entity))

    return entities

def get_feed_timestamp(feed):
    """Returns timestamps from th GTFS Realtime Feed Header as int"""
    return int(feed.header.timestamp)

def get_feed(feed_url):
    """Function to get GTFS Feed and Parse to List"""
    request_response = requests.get(feed_url)
    gtfs_feed = gtfs_realtime_pb2.FeedMessage()
    gtfs_feed.ParseFromString(request_response.content)
    return gtfs_feed


def main():
    """Main should only be called during testing"""
    print("Welcome to GTFSHandler.py")

    feed_url = "https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions"

    print(f"Feed URL: {feed_url}")
    print("Getting Feed")
    gtfs_feed = get_feed(feed_url)

    entities = get_entities(gtfs_feed)

    timestamp = get_feed_timestamp(gtfs_feed)

    for i in entities:
        print(f"Route ID: {i.get_route_id()}, Vehicle ID: {i.get_vehicle_id()}, Lat: {i.get_vehicle_position()[0]}, Long: {i.get_vehicle_position()[1]}")

    print(f"Timestamp: {timestamp}")

if __name__ == "__main__":
    main()
