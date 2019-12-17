#!/usr/bin/python

'''
creer un json gobable leafletjs, a partir d'une bdd sqlite
CREATE TABLE net (ID INTEGER PRIMARY KEY AUTOINCREMENT, ASYNCID INTEGER NOT NULL, STARTTIME INTEGER NOT NULL, ENDTIME INTEGER NOT NULL, HTTPREPLY INTEGER NOT NULL, NLOCS INTEGER NOT NULL, LAT REAL NOT NULL, LONG REAL NOT NULL);
CREATE TABLE loc (ID INTEGER PRIMARY KEY AUTOINCREMENT, FIXTIME INTEGER NOT NULL, LAT REAL NOT NULL, LONG REAL NOT NULL, ACC REAL NOT NULL, ALT REAL NOT NULL, ALTACC REAL NOT NULL, SENT INTEGER DEFAULT 0);
'''
 
import sqlite3
import json
import datetime
import sys
import time


#calcul epoch aujourdhui a minuit
#now = datetime.datetime.now()
#midnight_dt = datetime.datetime(year=now.year, month=now.month, day=now.day)
#epoch_minuit_ajd = int(time.mktime(midnight_dt.timetuple()))

#requete_net = 'SELECT asyncid, starttime, endtime, httpreply, nlocs, lat, long FROM net where starttime > ' + str(epoch_minuit_ajd)
#requete_loc = 'SELECT fixtime, lat, long, acc, alt, altacc, sent FROM loc where fixtime > ' + str(epoch_minuit_ajd)
requete_net = 'SELECT asyncid, starttime, endtime, httpreply, nlocs, lat, long FROM net'
requete_loc = 'SELECT fixtime, lat, long, acc, alt, altacc, sent FROM loc'
#requete_loc = 'SELECT fixtime, lat, long, acc, alt FROM loc'

db_file=str(sys.argv[1])


conn = sqlite3.connect(db_file)
cur = conn.cursor()





##Loc
cur.execute(requete_loc)
rows = cur.fetchall()
locs_array = []
length = len(rows) 

#epoch de minuit le jour du dernier fixtime
dt_last_day = datetime.datetime.fromtimestamp(rows[length-1][0]) #datetime du dernier fixtime
midnight_dt = datetime.datetime(year=dt_last_day.year, month=dt_last_day.month, day=dt_last_day.day) #datetime de minuit du jour du dernier fixtime
midnight_epoch = int(time.mktime(midnight_dt.timetuple())) #epoch de minuit le j du dernier fixtime


for i in range(length):
	#featureDict = {"asyncid":rows[i][0],"starttime":rows[i][1],"endtime":rows[i][2],"httpreply":rows[i][3],"nlocs":rows[i][4],"lat": rows[i][5], "long": rows[i][6]}
	featureDict = {"fixtime":rows[i][0],"lat":rows[i][1],"long":rows[i][2],"acc":rows[i][3],"alt":rows[i][4],"altacc": rows[i][5], "sent": rows[i][6]}
	#featureDict = {"fixtime":rows[i][0],"lat":rows[i][1],"long":rows[i][2],"acc":rows[i][3],"alt":rows[i][4]}
	if rows[i][0] > midnight_epoch:
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
	if rows[i][1]/1000 > midnight_epoch:
		net_array.append(featureDict)

outputfile.write("net_array ="+str(net_array))

print("data written to loctrack_data.js")
