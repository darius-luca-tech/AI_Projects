import json, os, wget, pandas as pd
from datetime import date, timedelta


with open("latestData.json") as f:
    data = json.load(f)

last_date = data["charts"]["dailyStats"]["lastUpdatedOn"]
last_date_year = int(last_date[0:4])
last_date_month = int(last_date[5:7])
last_date_day = int(last_date[8:])

print("{}-({}) {}-({}) {}-({})".format(last_date_year, type(last_date_year), last_date_month, type(last_date_month) ,last_date_day, type(last_date_day)))

def check():
    if os.path.exists("latestData.json"):
        os.remove("latestData.json")
    else:
        wget.download('https://datelazi.ro/latestData.json', '/home/gal1l30/Work/AI_Projects/Laura_Covid/')

    with open('latestData.json', 'r+') as f:
        data = json.load(f)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    f.close() 

start_date = date(2020, 4, 3)
end_date = date(last_date_year, last_date_month, last_date_day - 1)
delta = timedelta(days=1)


while(start_date <= end_date):
    # print(type(start_date.strftime("%Y-%m-%d")))
    date = start_date.strftime("%Y-%m-%d")
    start_date += delta

    with open("latestData.json") as f:
        data = json.load(f)
        data_wanted = data["historicalData"][date]["countyInfectionsNumbers"]

    with open("dataWanted.json", "a") as fp:
        fp.seek(0)
        json.dump(date, fp)
        json.dump(data_wanted, fp, indent=4)

with open("latestData.json") as f:
    data = json.load(f)
    data_wanted = data["currentDayStats"]["countyInfectionsNumbers"]

f.close()

with open("dataWanted.json", "a") as fp:
    fp.seek(0)
    json.dump(data_wanted, fp, indent=4)
# print(type(data["historicalData"]["2020-10-13"]["parsedOnString"]))
