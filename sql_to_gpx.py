#!/usr/bin/python

'''	
Parser loc.db android recupere avec tileview pour ne pas avoir des paquets enormes de locations aux memes endroits	
segreger des cluster par fixtime: on iterate, et quand le suivant est a plus que gap_time on finit un cluster, quon	
traite dans parse_un_cluster() -> on sort par accuracy.	
 ***Attention aux fixtime en milliseconde!!!***	
'''	

import sqlite3	
import json	
import os	
import time	
import calendar	
from osgeo import ogr	
from osgeo import gdal	


jour='29' #%d Day of the month as a decimal number [01,31].	
mois='07' #%m Month as a decimal number [01,12].	
annee='2019' #%Y Year with century as a decimal number.	
nombre_de_jours=1	


#la_db = '/initrd/mnt/dev_save/packages/GEO/playground_gdal/sample_dbs/loc_micisse.db'	
#la_db = '/initrd/mnt/dev_save/packages/GEO/loc-db_randos/lozere.db'	
la_db = '/root/loc.db'	
le_gpx="/root/"+jour+"_"+mois+".gpx"	

#https://docs.python.org/2/library/time.html	
#pour avoir epoch d'une date: date +%s -d 06.12-14:40	
#epoch_end = int(time.time()) #now...	

struct_epoch_start = time.strptime(jour + " " + mois + " " + annee, "%d %m %Y") 	
epoch_start = calendar.timegm(struct_epoch_start)	
epoch_end = epoch_start + (24 * nombre_de_jours * 3600)	



conn = sqlite3.connect(la_db)	
cur = conn.cursor()	
cur.execute("SELECT fixtime, lat, long, alt, acc FROM loc where FIXTIME > :epoch_start AND FIXTIME < :epoch_end", {"epoch_start": epoch_start, "epoch_end": epoch_end})	
rows = cur.fetchall()	



gap_time = 5 #delai au dela duquel je considere quon est dans un autre groupe de locations	
cluster_locations = [] #collection que tu arretes dalimenter quand le next fixtime est distant de + de gap_time	
final_locations = [] #destination finale des locations: parsage de chaque buffer location	


#A partir d un cluster de locations, en selectionner une seule (base sur accuracy je crois)	
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

#OK, a ce point on a les locations dans la collection "final_locations" au format:	
#	(1561526344, 43.93645806, 3.70691857, 237.0, 54.672000885009766) (epoch, lat, lng, ele, acc)	

outdriver = ogr.GetDriverByName('GPX')	
dataSourceOut = outdriver.CreateDataSource(le_gpx)	
outLayer = dataSourceOut.CreateLayer("track_points", geom_type=ogr.wkbPoint25D)	

#On fabrique les champs de la layer (cf custom_gpx.py)	
field_track_fid = ogr.FieldDefn("track_fid", ogr.OFTInteger)	
outLayer.CreateField(field_track_fid)	
field_track_seg_id = ogr.FieldDefn("track_seg_id", ogr.OFTInteger)	
outLayer.CreateField(field_track_seg_id)	
field_time = ogr.FieldDefn("time", ogr.OFTString)	
outLayer.CreateField(field_time)	
field_elev = ogr.FieldDefn("ele", ogr.OFTReal)	
outLayer.CreateField(field_elev)	





for loc in final_locations:	
	print time.strftime("%Y-%m-%d %H:%M:%S    ", time.localtime(loc[0])), loc[1], loc[2], int(loc[3]), int(loc[4]) 	
	point = ogr.Geometry(ogr.wkbPoint)	
	point.AddPoint(loc[2], loc[1])	
	outFeature = ogr.Feature(outLayer.GetLayerDefn())	
	outFeature.SetField("track_fid", "1")	
	outFeature.SetField("track_seg_id", "1")	
	outFeature.SetField("ele", loc[3])	
	outFeature.SetField("time", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(loc[0]))) #en UTC (greenwhich meridian) sinon time.localtime	
	outFeature.SetGeometry(point)	
	outLayer.CreateFeature(outFeature)	


print "nb total de fixes: ",len(final_locations) 	




outFeature = None	
dataSourceIn = None	
dataSourceOut = None
