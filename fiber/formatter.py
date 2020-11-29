import csv
import unicodedata
import json

from dbfread import DBF

insee_coms = set()
with open("result.csv", "w", newline="") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=";")
    spamwriter.writerow(["code_insee", "city_name"])
    for record in DBF('data.dbf', encoding="utf-8"):
        if record["INSEE_COM"] != "" and record["etat_trava"] == "Travaux en cours ou terminés":
            arrondissement = False
            for city_with_arrondissements in ["Paris", "Lyon", "Marseille"]:
                if "Arrondissement" in record["NOM_COM"] and record["NOM_COM"].startswith(city_with_arrondissements):
                    arrondissement = True
            if arrondissement:
                continue
            if record["INSEE_COM"] in insee_coms:
                continue
            insee_coms.add(record["INSEE_COM"])
            spamwriter.writerow([record["INSEE_COM"], record["NOM_COM"]])

    # very annoying to handle, added manually
    spamwriter.writerow([75056, "Paris"])
    spamwriter.writerow([13055, "Marseille"])
    spamwriter.writerow([69123, "Lyon"])