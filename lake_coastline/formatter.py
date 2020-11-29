import csv


with open("result.csv", "w", newline="") as result_file:
    spamwriter = csv.writer(result_file, delimiter=";")
    spamwriter.writerow(["code_insee", "city_name", "lake", "coastline"])
    with open('data.csv', newline='') as data_file:
        spamreader = csv.reader(data_file, delimiter=';')
        # multiple headers
        for i in range(0, 4):
            header = next(spamreader)
        for row in spamreader:
            lake = 1 if row[2] in ["TL", "ML", "PL"] else 0
            coastline = 1 if row[2] in ["TE", "TM", "PM"] else 0
            if lake or coastline:
                spamwriter.writerow([row[0], row[1], lake, coastline])