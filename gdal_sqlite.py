#!/usr/bin/python

'''
de sql lat long vers gpx 
https://gdal.org/drivers/vector/gpx.html
	Features of type wkbPoint/wkbPoint25D are written in the wpt element.
	Features of type wkbLineString/wkbLineString25D are written in the rte element.
	Features of type wkbMultiLineString/wkbMultiLineString25D are written in the trk element.

https://pcjericks.github.io/py-gdalogr-cookbook/index.html
https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#load-data-to-memory
'''
    
import os
from osgeo import ogr
from osgeo import gdal

indriver = ogr.GetDriverByName('SQLite')
dataSourceIn = indriver.Open("loc.db", 0) # 0 means read-only. 1 means writeable.

outdriver = ogr.GetDriverByName('GPX')
dataSourceOut = outdriver.CreateDataSource("out.gpx")

if dataSourceIn is None:
    print 'Could not open'
else:
    print 'Opened'
 
line = ogr.Geometry(ogr.wkbLineString) 
    
layer=dataSourceIn.GetLayer('loc') #nom de la table
for feature in layer:
    line.AddPoint(feature.GetField("LONG"), feature.GetField("LAT"), feature.GetField("ALT"))

print line.ExportToWkt()

#exporter line en gpx -> OK
#multilinestring https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#create-a-multilinestring

if dataSourceOut is None:
    print 'Could not get datasourceout'
else:
    print 'datasourceout ok'
    
multiline = ogr.ForceToMultiLineString(line)
print multiline.ExportToWkt()

outLayer = dataSourceOut.CreateLayer("un_nom", geom_type=ogr.wkbMultiLineString)
outLayerDefn = outLayer.GetLayerDefn()
outFeature = ogr.Feature(outLayerDefn)
outFeature.SetGeometry(multiline)
outLayer.CreateFeature(outFeature)

outFeature = None
dataSourceIn = None
dataSourceOut = None
