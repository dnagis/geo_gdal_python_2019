#!/usr/bin/python

'''
creer un json gobable leafletjs, a partir d'une bdd sqlite
CREATE TABLE net (ID INTEGER PRIMARY KEY AUTOINCREMENT, ASYNCID INTEGER NOT NULL, STARTTIME INTEGER NOT NULL, ENDTIME INTEGER NOT NULL, HTTPREPLY INTEGER NOT NULL, NLOCS INTEGER NOT NULL, LAT REAL NOT NULL, LONG REAL NOT NULL);
CREATE TABLE loc (ID INTEGER PRIMARY KEY AUTOINCREMENT, FIXTIME INTEGER NOT NULL, LAT REAL NOT NULL, LONG REAL NOT NULL, ACC REAL NOT NULL, ALT REAL NOT NULL, ALTACC REAL NOT NULL, SENT INTEGER DEFAULT 0);
'''
 
import sqlite3
import json
from datetime import datetime

#requete_sqlite = 'SELECT asyncid, starttime, endtime, httpreply, nlocs, lat, long FROM net'
requete_sqlite = 'SELECT fixtime, lat, long, acc, alt, altacc, sent FROM loc'

db_file = '/root/loc.db'
conn = sqlite3.connect(db_file)
cur = conn.cursor()
cur.execute(requete_sqlite)
rows = cur.fetchall()


array_final = []

length = len(rows) 

for i in range(length):
	#featureDict = {"asyncid":rows[i][0],"starttime":rows[i][1],"endtime":rows[i][2],"httpreply":rows[i][3],"nlocs":rows[i][4],"lat": rows[i][5], "long": rows[i][6]}
	featureDict = {"fixtime":rows[i][0],"lat":rows[i][1],"long":rows[i][2],"acc":rows[i][3],"alt":rows[i][4],"altacc": rows[i][5], "sent": rows[i][6]}
	array_final.append(featureDict)


#utiliser du ternary?
print "locs_array =",array_final


