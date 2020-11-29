import csv
import json
import os
import requests
import ssl
from multiprocessing import Pool

SNCF_API_TOKEN = "7b55fe07-6a4c-4b10-a1b8-909e5e12b5f0"
# SNCF_API_TOKEN = "16607842-543c-4bc8-807f-73a1b8c5695f"
# SNCF_API_TOKEN = "eec588d2-c133-419f-83de-8fc595fb6a4f"
CODES_INSEE = {
    "marseille": 13055,
    "lyon": 69123,
    "paris": 75056,
}
FROM_INSEE_CODE = 13055
FROM = "admin:fr:" + str(FROM_INSEE_CODE)
API_RESPONSES_CITIES_PATH = "api_responses/cities/"
API_RESPONSES_TRAVEL_TIMES_PATH = "api_responses/travel_times/"

def getTrainStations():
    print("getting cities...")
    train_stations = []
    train_station_ids = []
    with open("data.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";")
        next(csvfile)
        for row in spamreader:
            if row[0] in train_station_ids:  # ignore duplicates
                continue
            if row[3] != "O":  # ignore stations not opened to the public
                continue
            train_stations.append({
                "id": row[0],
                "name": row[1],
                "lng": row[13],
                "lat": row[14],
            })
            train_station_ids.append(row[0])
    with Pool(8) as p:
        api_responses = p.map(getTrainStationCity, train_stations)
    result = []
    for index, train_station in enumerate(train_stations):
        with open(f"{API_RESPONSES_CITIES_PATH}{train_station['id']}.json", "w") as api_response_file:
            api_response_file.write(json.dumps(api_responses[index]))
        try:
            city_name = api_responses[index][0]["nom"]
            code_insee = api_responses[index][0]["code"]
        except KeyError:
            print(f"could not find city for station {row[1]}")
            continue
        train_station["city_name"] = city_name
        train_station["code_insee"] = code_insee
        result.append(train_station)
    print(f"done, {len(train_stations)} train stations")
    return train_stations

def getTrainStationCity(train_station):
    if os.path.isfile(f"{API_RESPONSES_CITIES_PATH}{train_station['id']}.json"):
        with open(f"{API_RESPONSES_CITIES_PATH}{train_station['id']}.json", "r") as api_response_file:
            data = api_response_file.read()
            return json.loads(data)
    response = requests.get(f"https://geo.api.gouv.fr/communes?lat={train_station['lat']}&lon={train_station['lng']}&fields=om,code,codesPostaux,centre,surface,contour,codeDepartement,departement,codeRegion,region&format=json&geometry=centre")
    response_json = response.json()
    return response_json

def getStationsTravelTimes(train_stations):
    print(f"getting travel times...")
    with Pool(8) as p:
        api_responses = p.map(getStationTravelTime, train_stations)
    result = []
    for index, train_station in enumerate(train_stations):
        with open(f"{API_RESPONSES_TRAVEL_TIMES_PATH}{FROM}__{train_station['id']}.json", "w") as api_response_file:
            api_response_file.write(json.dumps(api_responses[index]))
        try:
            travel_time = api_responses[index]["journeys"][0]["duration"]/60/60
            itinerary = getJourneyItinerary(api_responses[index]["journeys"][0])
        except KeyError:
            print(f"no journeys to {train_station['name']}")
            continue
        train_station = train_stations[index]
        train_station["travel_time"] = travel_time
        train_station["itinerary"] = json.dumps(itinerary)
        train_station["from"] = FROM_INSEE_CODE
        result.append(train_station)
    print(f"done, {len(result)} train stations")
    return result

def getJourneyItinerary(journey):
    itinerary = {
        "type": "LineString",
        "coordinates": []
    }
    for section in journey["sections"]:
        try:
            itinerary["coordinates"].extend(section["geojson"]["coordinates"])
        except KeyError:  # no geojson for given section
            continue
    return itinerary

def getStationTravelTime(train_station):
    if os.path.isfile(f"{API_RESPONSES_TRAVEL_TIMES_PATH}{FROM}__{train_station['id']}.json"):
        with open(f"{API_RESPONSES_TRAVEL_TIMES_PATH}{FROM}__{train_station['id']}.json", "r") as api_response_file:
            data = api_response_file.read()
            return json.loads(data)
    response = requests.get(f"https://{SNCF_API_TOKEN}:@api.sncf.com/v1/coverage/sncf/journeys?from={FROM}&to=stop_area:OCE:SA:{train_station['id']}")
    response_json = response.json()
    return response_json

def saveTravelTimes(train_stations):
    with open("result.csv", "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";")
        spamwriter.writerow(train_stations[0].keys())
        for train_station in train_stations:
            spamwriter.writerow(train_station.values())

if __name__ == "__main__":
    train_stations = getTrainStations()
    train_stations = getStationsTravelTimes(train_stations)
    saveTravelTimes(train_stations)