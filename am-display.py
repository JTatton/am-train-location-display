from csv import reader

def loadStops():
    print("Loading Stops")
    with open('station-info.csv', 'r') as readObj:
        csvReader = reader(readObj)
        listOfStations = list(csvReader)
    
    for station in listOfStations:
        print(station[0], ":", station[1], ", ", station[2])

loadStops()