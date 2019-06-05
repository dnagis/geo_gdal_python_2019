#!/usr/bin/python

'''
Parser loc.db android recupere avec tileview pour ne pas avoir des paquets enormes de locations aux memes endroits
segreger des cluster par fixtime: on iterate, et quand le suivant est a plus que gap_time on finit un cluster, quon
traite dans parse_un_cluster() -> on sort par accuracy.
'''
 
import sqlite3
import json
from datetime import datetime
import os
from osgeo import ogr
from osgeo import gdal


#la_db = '/initrd/mnt/dev_save/packages/GEO/playground_gdal/sample_dbs/loc_micisse.db'
la_db = '/root/lozere.db'
le_gpx = '/root/out.gpx'
conn = sqlite3.connect(la_db)
cur = conn.cursor()
cur.execute("SELECT fixtime, lat, long, alt, acc FROM loc WHERE ID > 30")
rows = cur.fetchall()







gap_time = 60 #delai au dela duquel je considere quon est dans un autre groupe de locations
cluster_locations = [] #collection que tu arretes dalimenter quand le next fixtime est distant de + de gap_time
final_locations = [] #destination finale des locations: parsage de chaque buffer location

featureDict = {
  'geometry': { 'type': 'Point', 'coordinates': [None, None] },
  "type": "Feature",
  "properties": {"popupContent": None}
}




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


    
line = ogr.Geometry(ogr.wkbLineString)
for loc in final_locations:
	line.AddPoint(loc[2], loc[1], loc[3])
multiline = ogr.ForceToMultiLineString(line)
outdriver = ogr.GetDriverByName('GPX')
dataSourceOut = outdriver.CreateDataSource(le_gpx)
outLayer = dataSourceOut.CreateLayer("lozere", geom_type=ogr.wkbMultiLineString)
outLayerDefn = outLayer.GetLayerDefn()
outFeature = ogr.Feature(outLayerDefn)
outFeature.SetGeometry(multiline)
outLayer.CreateFeature(outFeature)
outFeature = None
dataSourceIn = None
dataSourceOut = None


    
    

