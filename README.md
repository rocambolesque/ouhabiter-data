Data extraction module

## open data
transport/data.csv: https://data.sncf.com/explore/dataset/referentiel-gares-voyageurs/table/?disjunctive.gare_ug_libelle&sort=gare_alias_libelle_noncontraint
fiber/data.dbf: https://www.data.gouv.fr/fr/datasets/le-marche-du-haut-et-tres-haut-debit-fixe-deploiements/
population/data.csv: https://www.insee.fr/fr/statistiques/4265429?sommaire=4265511, file Communes.csv
mountains/data.csv: https://www.observatoire-des-territoires.gouv.fr/typologie-des-montagnes
sea_lakes/data.csv: https://www.observatoire-des-territoires.gouv.fr/modalites-du-classement-des-communes-en-loi-littoral
countryside/data.csv: https://www.observatoire-des-territoires.gouv.fr/typologie-des-campagnes-francaises-champ-paysages
park/data.csv: https://www.observatoire-des-territoires.gouv.fr/perimetre-des-parcs-naturels-regionaux-pnr

## "communes" and cities
we'll only consider cities basically eliminating arrondissements for Paris, Lyon and Marseille

## modules
each module contains a raw data file in whatever format was made available (csv, dbf)
each module contains a formatter which extracts data used for this project from the data file and dumps it in a result.csv file

transport: travel times by train from a point of origin to all train stations in France
fiber: cities equipped with fiber internet
population: cities' population numbers
mountains: mountain cities
sea_lake: cities close on the coastline or close to a lake
countryside: cities located in the countryside
park: cities localed in a regional nature park

## todo list
parks: add national nature parks

## how to use
execute merge.py to intersect everything