#!/usr/bin/python

'''
https://gdal.gloobe.org/python/intro_vecteur.html
'''
    
import os
import json
from osgeo import ogr
from osgeo import gdal



#Creation d'un shapefile de points
driver = ogr.GetDriverByName('ESRI Shapefile')
ds = driver.CreateDataSource('monShapefile.shp')
layer = ds.CreateLayer('monShapefile', geom_type=ogr.wkbPoint)

#
feature_def=layer.GetLayerDefn()
f = ogr.Feature(feature_def)

# Ajout du point
x = 731065
y = 2368493
wkt = 'POINT(%f %f)' % (x, y)
p = ogr.CreateGeometryFromWkt(wkt)
f.SetGeometryDirectly(p)
layer.CreateFeature(f)

f.Destroy()
