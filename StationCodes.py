import csv
reader = csv.reader(open('station_codes.csv'))
station_to_crs = {}
crs_to_station = {}
for row in reader:
    key0 = row[0]
    key1 = row[1]
    station_to_crs[key0] = row[1]
    crs_to_station[key1] = row[0]