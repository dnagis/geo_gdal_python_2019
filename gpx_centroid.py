#!/usr/bin/python

'''
https://pcjericks.github.io/py-gdalogr-cookbook/index.html
ouvrir un gpx, recuperer les features, creer un multipoint, avoir son centroid en json
'''
    
import os
from osgeo import ogr
from osgeo import gdal

driver = ogr.GetDriverByName('GPX')

dataSource = driver.Open("4000Marches.gpx", 0) # 0 means read-only. 1 means writeable.

if dataSource is None:
    print 'Could not open'
else:
    print 'Opened'
    layer = dataSource.GetLayer("track_points")
    featureCount = layer.GetFeatureCount()
    print "Number of features in %s: %d" % (os.path.basename("4000Marches.gpx"),featureCount)
    multipoint = ogr.Geometry(ogr.wkbMultiPoint) 
    for feature in layer:
		geom = feature.GetGeometryRef()
		print geom.Centroid().ExportToWkt()
		multipoint.AddGeometry(geom.Centroid())
    print 'centroid = ' + multipoint.Centroid().ExportToWkt()
    geojson = multipoint.ExportToJson()
    print geojson
