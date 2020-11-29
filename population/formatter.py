import csv

paris_population = 0
marseille_population = 0
lyon_population = 0

with open("result.csv", "w", newline="") as result_file:
    spamwriter = csv.writer(result_file, delimiter=";")
    spamwriter.writerow(["code_insee", "city_name", "population"])
    with open('data.csv', newline='') as data_file:
        spamreader = csv.reader(data_file, delimiter=';')
        header = next(spamreader)
        for row in spamreader:
            if "Arrondissement" in row[1]:
                if "Paris" in row[1]:
                    paris_population += int(row[4])
                elif "Marseille" in row[1]:
                    marseille_population += int(row[4])
                elif "Lyon" in row[1]:
                    lyon_population += int(row[4])
            else:
                spamwriter.writerow([row[0], row[1], row[4]])
    spamwriter.writerow([75056, "Paris", paris_population])
    spamwriter.writerow([13055, "Marseille", marseille_population])
    spamwriter.writerow([69123, "Lyon", lyon_population])