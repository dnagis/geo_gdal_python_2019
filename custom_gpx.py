#!/usr/bin/python

'''
But= customiser le gpx -> balise <time> pour chaque <trkpt>, comme dans les exemples de visugpx.com

https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#iterate-over-features
https://gdal.org/python/osgeo.ogr.Feature-class.html -->GetFieldAsDateTime(self, *args)

https://gdal.org/drivers/vector/gpx.html --> surtout la partie qui contient track_fid etc...

ToDo: ajouter l'heure, l elevation, et ***surtout*** des commentaires comme s'il en pleuvait+++


'''

import time
import os
from osgeo import ogr
from osgeo import gdal


outdriver = ogr.GetDriverByName('GPX')
dataSourceOut = outdriver.CreateDataSource("/root/outgpxtime.gpx")
#https://gdal.org/drivers/vector/gpx.html 

#On cree une layer de features, on l'apl "track_points" pour avoir <trk> -> the tracks in the GPX file will be built from the sequence of features in that layer
outLayer = dataSourceOut.CreateLayer("track_points", geom_type=ogr.wkbPoint25D)

#On fabrique les champs de la layer
#Deux premiers fields obligatoires: comme on a cree une layer de tracks, 
# tu mets un int dedans, du moment qu'il est le meme les points seront dans la meme track
# cf. https://gdal.org/drivers/vector/gpx.html
field_track_fid = ogr.FieldDefn("track_fid", ogr.OFTInteger)
outLayer.CreateField(field_track_fid)
field_track_seg_id = ogr.FieldDefn("track_seg_id", ogr.OFTInteger)
outLayer.CreateField(field_track_seg_id)
field_time = ogr.FieldDefn("time", ogr.OFTString)
outLayer.CreateField(field_time)
field_elev = ogr.FieldDefn("ele", ogr.OFTReal)
outLayer.CreateField(field_elev)




lat = 43.944026
lng = 3.717440
elevation = 231.5
epoch = 1561571994
str_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(epoch))
point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(lng, lat)

#Une "feature" cest une geometry avec des donnees associees -> on fabrique une feature...
outFeature = ogr.Feature(outLayer.GetLayerDefn())
outFeature.SetField("track_fid", "1")
outFeature.SetField("track_seg_id", "1")
outFeature.SetField("ele", elevation)
outFeature.SetField("time", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(epoch)))
outFeature.SetGeometry(point)
#et on lajoute a la layer
outLayer.CreateFeature(outFeature)


outFeature = None
dataSourceIn = None
dataSourceOut = None
