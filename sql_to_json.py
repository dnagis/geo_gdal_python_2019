#!/usr/bin/python

'''
creer un json gobable leafletjs, a partir d'une bdd sqlite
'''
 
import sqlite3
import json
from datetime import datetime

db_file = '/root/loc.db'
conn = sqlite3.connect(db_file)
cur = conn.cursor()
cur.execute("SELECT fixtime, lat, long, alt, acc FROM loc")
rows = cur.fetchall()


locs_array = []

length = len(rows) 

for i in range(length-1):
	featureDict = {"lat": rows[i][1], "long": rows[i][2]}
	locs_array.append(featureDict)


print "locs_array =",locs_array


