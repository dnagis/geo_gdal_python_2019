#!/usr/bin/python

'''
creer un json gobable leafletjs, a partir d'une bdd sqlite
CREATE TABLE net (ID INTEGER PRIMARY KEY AUTOINCREMENT, ASYNCID INTEGER NOT NULL, STARTTIME INTEGER NOT NULL, ENDTIME INTEGER NOT NULL, HTTPREPLY INTEGER NOT NULL, NLOCS INTEGER NOT NULL, LAT REAL NOT NULL, LONG REAL NOT NULL);
'''
 
import sqlite3
import json
from datetime import datetime

db_file = '/root/loc.db'
conn = sqlite3.connect(db_file)
cur = conn.cursor()
cur.execute("SELECT asyncid, starttime, endtime, httpreply, nlocs, lat, long FROM net")
rows = cur.fetchall()


locs_array = []

length = len(rows) 

for i in range(length):
	featureDict = {"asyncid":rows[i][0],"starttime":rows[i][1],"endtime":rows[i][2],"httpreply":rows[i][3],"nlocs":rows[i][4],"lat": rows[i][5], "long": rows[i][6]}
	locs_array.append(featureDict)


print "net_array =",locs_array


