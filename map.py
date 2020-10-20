import sqlite3
import urllib.request, urllib.parse, urllib.error
import json

conn = sqlite3.connect('beijingmap.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS houseprice (id INTEGER PRIMARY KEY, name TEXT UNIQUE, lng varchar(30), lat varchar(30), count integer, price integer, border text)''')

#fullmaxlong = 116.76
fullminlong = 116.01
#fullmaxlat = 40.25
fullminlat = 39.65

minlong = fullminlong
minlat = fullminlat
maxlong = minlong + 0.15
maxlat = minlat + 0.1

#a maximum of 100 items are listed in a single search
#sliding windows to make sure all regions are captured

baseurl = 'https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId=110000&dataSource=ESF&condition=&id=&groupType=bizcircle&maxLatitude='


for i in range(30):
	url = baseurl + str(maxlat) + '&minLatitude=' + str(minlat) + '&maxLongitude=' + str(maxlong) + '&minLongitude=' + str(minlong)
	raw = urllib.request.urlopen(url)
	data = raw.read()

	try:
		js = json.loads(data)
	except:
		js = None

	if "bubbleList" in js["data"]:
		for item in js["data"]["bubbleList"]:
			name = item["name"]
			lng = item["longitude"]
			lat = item["latitude"]
			count = item["count"]
			price = item["price"]
			border = item["border"]
			ls = [name,lng,lat,count,price,border]
			cur.execute('''INSERT OR IGNORE INTO houseprice (name,lng,lat,count,price,border) VALUES (?,?,?,?,?,?)''', ls)
			conn.commit()
	minlong = maxlong
	maxlong = minlong + 0.15
	if maxlong > 116.77:
		minlong = fullminlong
		maxlong = minlong+0.15
		minlat = maxlat
		maxlat = minlat +0.1
	#print(minlong)


