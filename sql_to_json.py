#!/usr/bin/python

'''
creer un json gobable leafletjs, a partir d'une bdd sqlite
CREATE TABLE net (ID INTEGER PRIMARY KEY AUTOINCREMENT, ASYNCID INTEGER NOT NULL, STARTTIME INTEGER NOT NULL, ENDTIME INTEGER NOT NULL, HTTPREPLY INTEGER NOT NULL, NLOCS INTEGER NOT NULL, LAT REAL NOT NULL, LONG REAL NOT NULL);
CREATE TABLE loc (ID INTEGER PRIMARY KEY AUTOINCREMENT, FIXTIME INTEGER NOT NULL, LAT REAL NOT NULL, LONG REAL NOT NULL, ACC REAL NOT NULL, ALT REAL NOT NULL, ALTACC REAL NOT NULL, SENT INTEGER DEFAULT 0);
'''
 
import sqlite3
import json
from datetime import datetime
import sys



requete_net = 'SELECT asyncid, starttime, endtime, httpreply, nlocs, lat, long FROM net'
requete_loc = 'SELECT fixtime, lat, long, acc, alt, altacc, sent FROM loc'

db_file=str(sys.argv[1])


conn = sqlite3.connect(db_file)
cur = conn.cursor()


##Loc
cur.execute(requete_loc)
rows = cur.fetchall()
locs_array = []
length = len(rows) 

for i in range(length):
	#featureDict = {"asyncid":rows[i][0],"starttime":rows[i][1],"endtime":rows[i][2],"httpreply":rows[i][3],"nlocs":rows[i][4],"lat": rows[i][5], "long": rows[i][6]}
	featureDict = {"fixtime":rows[i][0],"lat":rows[i][1],"long":rows[i][2],"acc":rows[i][3],"alt":rows[i][4],"altacc": rows[i][5], "sent": rows[i][6]}
	locs_array.append(featureDict)


outputfile = open("loctrack_data.js", "w+") 
outputfile.write("locs_array ="+str(locs_array)+"\n")


##network
cur.execute(requete_net)
rows = cur.fetchall()
length = len(rows)
net_array = []
for i in range(length):
	featureDict = {"asyncid":rows[i][0],"starttime":rows[i][1],"endtime":rows[i][2],"httpreply":rows[i][3],"nlocs":rows[i][4],"lat": rows[i][5], "long": rows[i][6]}
	net_array.append(featureDict)

outputfile.write("net_array ="+str(net_array))
