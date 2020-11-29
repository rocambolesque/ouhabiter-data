import csv


with open("result.csv", "w", newline="") as result_file:
    spamwriter = csv.writer(result_file, delimiter=";")
    spamwriter.writerow(["code_insee", "city_name"])
    with open('data.csv', newline='') as data_file:
        spamreader = csv.reader(data_file, delimiter=';')
        # multiple headers
        for i in range(0, 4):
            header = next(spamreader)
        for row in spamreader:
            if row[2] != "99":
                spamwriter.writerow([row[0], row[1], row[4]])