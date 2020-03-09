from datetime import date, datetime
import csv
import requests


today = date.today()
print(f"Getting data for: {today}")

r = requests.get("https://services.arcgis.com/5T5nSi527N4F7luB/arcgis/rest/services/COVID_19_CasesByCountry(pl)_VIEW/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*")

with open(f"../data/json/json-{today}.txt", "w") as json_file:
    json_file.write(r.text)

jdata = r.json()
features = [f["attributes"] for f in jdata["features"]]
features = [{ "DateOfReport":  datetime.utcfromtimestamp(f["DateOfReport"] / 1000).strftime("%Y-%m-%d"),
    "ADM0_VIZ_NAME": f["ADM0_VIZ_NAME"], 
    "Short_Name_ZH": f["Short_Name_ZH"],
    "cum_conf": f["cum_conf"],
    "cum_death": f["cum_death"] } for f in features]

with open(f"../data/csv/csv-{today}.csv", "w", newline="") as csv_file:
    fieldnames = ["DateOfReport", "ADM0_VIZ_NAME", "Short_Name_ZH", "cum_conf", "cum_death"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for f in features:
        writer.writerow(f)

print("Done.")

