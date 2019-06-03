#!/usr/bin/python

#https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#write-geometry-to-geojson
    
import os
from osgeo import ogr
from osgeo import gdal

multipoint = ogr.Geometry(ogr.wkbMultiPoint)

point1 = ogr.Geometry(ogr.wkbPoint)
point1.AddPoint(3.63573,44.09597)
multipoint.AddGeometry(point1)

point2 = ogr.Geometry(ogr.wkbPoint)
point2.AddPoint(3.63586,44.09372)
multipoint.AddGeometry(point2)

point3 = ogr.Geometry(ogr.wkbPoint)
point3.AddPoint(3.63551,44.09264)
multipoint.AddGeometry(point3)

print multipoint.ExportToWkt()

geojson = multipoint.ExportToJson()
print geojson
