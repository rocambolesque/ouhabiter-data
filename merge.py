import csv
import json
import requests
import unicodedata


train_stations = []
with open('transport/result.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    header = next(spamreader)
    for row in spamreader:
        train_stations.append(row)
print(f"{len(train_stations)} train stations")

cities = {}
# population first to have a complete list of cities
with open('population/result.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    header = next(spamreader)
    for row in spamreader:
        cities[row["code_insee"]] = row
print(f"{len(cities.keys())} cities")

for option in ["mountains", "fiber", "lake_coastline", "countryside", "park"]:
    with open(f"{option}/result.csv", newline="") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=";")
        header = next(spamreader)
        for row in spamreader:
            try:
                if option == "lake_coastline":
                    cities[row["code_insee"]]["lake"] = True if row["lake"] == "1" else False
                    cities[row["code_insee"]]["coastline"] = True if row["coastline"] == "1" else False
                else:
                    cities[row["code_insee"]][option] = True
            except KeyError:  # skip cities missing population
                continue

print("merging...")
json_content = []
for train_station in train_stations:
    try:
        city = cities[train_station[5]]
    except KeyError:  # train station in a city that was filtered out
        continue
    city_name = unicodedata.normalize('NFD', train_station[4]).encode('ascii', 'ignore').decode("utf-8")
    station_name = unicodedata.normalize('NFD', train_station[1]).encode('ascii', 'ignore').decode("utf-8")
    json_item = {
        'stationId': int(train_station[0]),
        'lng': float(train_station[2]),
        'lat': float(train_station[3]),
        'toCityInseeCode': int(train_station[5]),
        'travelTime': float(train_station[6]),
        'fromCityInseeCode': int(train_station[8]),
        'stationName': station_name,
        'cityName': city_name,
        'cityPopulation': int(city["population"]),
        'hasMountains': city.get("mountains", False),
        'hasFiber': city.get("fiber", False),
        'hasLake': city.get("lake", False),
        'hasCoastline': city.get("coastline", False),
        'hasCountryside': city.get("countryside", False),
        'hasPark': city.get("park", False),
    }
    json_content.append(json_item)
print(f"total: {len(json_content)} train stations")

with open("result.json", "w") as jsonfile:
    jsonfile.write(json.dumps(json_content, indent=2))
print("done")