#!/usr/bin/python

'''
creer des features de toutes pieces, et les append a un array 
pour avoir un json final gobable par leafletjs
'''
    
import os
import json
from osgeo import ogr
from osgeo import gdal


#datasource pour creer layer, indispensable pour setField, et feature defn pour creer feature
monDriver=ogr.GetDriverByName('MEMORY')
ds=monDriver.CreateDataSource('memData')
maLayer = ds.CreateLayer("maLayer", geom_type=ogr.wkbPoint)

# Add a popupContent field
popField = ogr.FieldDefn("popupContent", ogr.OFTString)
maLayer.CreateField(popField)



feature_defn = maLayer.GetLayerDefn()



f1 = ogr.Feature(feature_defn)
f1.SetField("popupContent", "zob")
wkt1 = "POINT (1.4399 42.6148)"
point1 = ogr.CreateGeometryFromWkt(wkt1)
f1.SetGeometry(point1)


f2 = ogr.Feature(feature_defn)
f2.SetField("popupContent", "zob2")
wkt2 = "POINT (1.4300 42.6147)"
point2 = ogr.CreateGeometryFromWkt(wkt2)
f2.SetGeometry(point2)






feature_collection = []

#sans as_object ya des " partout c'est lhorreur
feature_collection.append(f1.ExportToJson(as_object=True))
feature_collection.append(f2.ExportToJson(as_object=True))

#maLayer.CreateFeature(f1)

#print f1.ExportToJson()

print json.dumps(feature_collection)


