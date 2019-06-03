#!/usr/bin/python


'''
prendre des gpx, les ouvrir avec gdal via le driver gpx -> datasource -> track point layer (tp_layer)
	y recuperer le nom de la rando et fabriquer un multipoint pour avoir son centroid()
fabriquer une layer de toutes pieces (driver memory, datasource, field popupContent pour leafletjs)
	pour chaque rando je cree une feature, jy mets le nom dans le field popupcontent et
	dans geometry le centroid des points de la rando.
jappend chaque feature a un array feature_collection (ou une list je sais pas trop) 
	
'''


import os
import json
from osgeo import ogr
from osgeo import gdal


#on recupere tous les fichiers .gpx dans allgpxfiles
path = '/initrd/mnt/dev_save/packages/GEO/cnsnmm'

allgpxfiles = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.gpx' in file:
            allgpxfiles.append(os.path.join(r, file))


drivergpx = ogr.GetDriverByName('GPX')
#mp_ttes_randos = ogr.Geometry(ogr.wkbMultiPoint) #les points des centroid de toutes les randos (1 par rando)

#Oblige davoir layer pas gpx pour ajouter un field popupcontent
driverdummy=ogr.GetDriverByName('MEMORY')
ds=driverdummy.CreateDataSource('memData')
maLayer = ds.CreateLayer("maLayer", geom_type=ogr.wkbPoint)
popField = ogr.FieldDefn("popupContent", ogr.OFTString)
maLayer.CreateField(popField)
malayer_defn = maLayer.GetLayerDefn() #jen ai besoin pour creer une feature


feature_collection = []


for f in allgpxfiles:
    dataSource = drivergpx.Open(f, 0)
    tp_layer = dataSource.GetLayer("track_points")
    namestring_rando = dataSource.GetLayer("tracks")[0].GetField("name")
    #print namestring_rando
    #print "Number of features : %d" % tp_layer.GetFeatureCount()
    mp_one_rando = ogr.Geometry(ogr.wkbMultiPoint) #le multipoint pour une rando, a partir duquel on recupere le centroid
    for feature in tp_layer:
	    geom = feature.GetGeometryRef()		
	    mp_one_rando.AddGeometry(geom.Centroid())
    ma_feature = ogr.Feature(malayer_defn)
    ma_feature.SetField("popupContent", namestring_rando)
    ma_feature.SetGeometry(mp_one_rando.Centroid())
    #mp_ttes_randos.AddGeometry(mp_one_rando.Centroid())
    feature_collection.append(ma_feature.ExportToJson(as_object=True))

#geojson = mp_ttes_randos.ExportToJson()
#print geojson

print json.dumps(feature_collection)



