#!/usr/bin/python

'''
Parser loc.db android recupere avec tileview pour ne pas avoir des paquets enormes de locations aux memes endroits
segreger des cluster par fixtime: on iterate, et quand le suivant est a plus que gap_time on finit un cluster, quon
traite dans parse_un_cluster() -> on sort par accuracy.
'''
 
import sqlite3
import json
from datetime import datetime


#la_db = '/initrd/mnt/dev_save/packages/GEO/playground_gdal/sample_dbs/loc_micisse.db'
la_db = '/root/lozere.db'
conn = sqlite3.connect(la_db)
cur = conn.cursor()
cur.execute("SELECT fixtime, lat, long, alt, acc FROM loc")
rows = cur.fetchall()


#for row in rows:
#    print(row)

gap_time = 60 #delai au dela duquel je considere quon est dans un autre groupe de locations
cluster_locations = [] #collection que tu arretes dalimenter quand le next fixtime est distant de + de gap_time
final_locations = [] #destination finale des locations: parsage de chaque buffer location

featureDict = {
  'geometry': { 'type': 'Point', 'coordinates': [None, None] },
  "type": "Feature",
  "properties": {"popupContent": None}
}

def location_tuples_to_json(locs): #locs = list of tuples
	feature_list = []
	for loc in locs:
		print loc
		featureDict = {
			'geometry': { 'type': 'Point', 'coordinates': [loc[2], loc[1]] },
			"type": "Feature",
			"properties": {"popupContent": datetime.fromtimestamp(loc[0]).strftime('%Y-%m-%d %H:%M:%S') + " elev:" + str(loc[3])}
			}
		feat_json = json.dumps(featureDict)
		feature_list.append(feat_json)
	print("[" + ', '.join(feature_list) + "]")
	


def parse_un_cluster(un_cluster):
	#print "on parse un cluster sa taille= ",len(un_cluster)
	#print un_cluster
	cluster_sorted = sorted(un_cluster, key = lambda x: x[4])
	best_loc_du_cluster = cluster_sorted[0]
	#print best_loc_du_cluster
	final_locations.append(best_loc_du_cluster)
	
    
length = len(rows)   

#print "nb total de rows dans le fichier: ",length  

for i in range(length-1): #on pourrait commencer a 1 avec range(1, n)
    #print rows[i]
    cluster_locations.append(rows[i])
    diff = int(rows[i+1][0] - rows[i][0]) 
    #print diff
    if diff > gap_time:
        parse_un_cluster(cluster_locations)
        cluster_locations = [] # on repart a zero
    

location_tuples_to_json(final_locations)
#print final_locations 
    
    

