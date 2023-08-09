#!/usr/bin/python

from google.transit import gtfs_realtime_pb2
import urllib.request
import matplotlib.pyplot as plt
import math
import time

longs = []
lats = []
long_new = []
lat_new = []

plt.ion()

#fig, ax = plt.subplots(figsize = (8,7))
fig, ax = plt.subplots()

lims =  [138.4360, 138.7971, -35.2075, -34.5676]

ax.set_xlim(lims[0],lims[1])
ax.set_ylim(lims[2],lims[3])

#feed = gtfs_realtime_pb2.FeedMessage()
#response = urllib.request.urlopen('https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions')
#feed.ParseFromString(response.read())

#img = plt.imread("map.png")
#ax.imshow(img, zorder=0, extent = lims, aspect= 'equal')

while(True):

    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.request.urlopen('https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions')
    feed.ParseFromString(response.read())

    img = plt.imread("map.png")
    ax.imshow(img, zorder=0, extent = lims, aspect= 'equal')
    longs = []
    lats = []

    for entity in feed.entity:
        if entity.HasField('vehicle'):
            if entity.vehicle.vehicle.id.startswith("40") or entity.vehicle.vehicle.id.startswith("30") or entity.vehicle.vehicle.id.startswith("31"):
                veh_id = entity.vehicle.vehicle.id
                longitude = entity.vehicle.position.longitude
                latitude = entity.vehicle.position.latitude
                bearing = entity.vehicle.position.bearing
                speed = entity.vehicle.position.speed

                vector_long = (speed/1000 * math.sin(math.radians(bearing)))
                vector_lat = (speed/1000 * math.cos(math.radians(bearing)))

                longs.append(longitude)
                lats.append(latitude)

                #ax.arrow(longitude, latitude, vector_long, vector_lat, head_width=0.005, head_length=0.01, fc='k', ec='k')
                ax.annotate(str(veh_id), (longitude, latitude))
                scat= ax.scatter(longs, lats, zorder=1, alpha= 1, c='b', s=20)
                plt.draw()
    
    plt.show()
    print("Start Pause")
    plt.pause(20)
    print("End pause")
    scat.remove()
    plt.draw()
    plt.show()


#img = plt.imread("map.png")


#ax.scatter(longs, lats, zorder=1, alpha= 1, c='b', s=20)
#ax.arrow(longs,lats,long_new,lat_new, head_width=0.05, head_length=0.1, fc='k', ec='k')

#img = plt.imread("map.png")
#ax.imshow(img, zorder=0, extent = lims, aspect= 'equal')

#plt.show()
#plt.draw() 
#plt.pause(0.01)
#print("Start Sleep")
#plt.pause(20)
#print("End Sleep")
#plt.clf()