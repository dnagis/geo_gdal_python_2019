#!/usr/bin/python

'''
de sql lat long vers json 
'''
    
import os
import json
from osgeo import ogr
from osgeo import gdal

indriver = ogr.GetDriverByName('SQLite')
dataSourceIn = indriver.Open("loc.db", 0) # 0 means read-only. 1 means writeable.

if dataSourceIn is None:
    print 'Could not open'

 

    
layer=dataSourceIn.GetLayer('loc') #nom de la table

feature_collection = []

for feature in layer:
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(feature.GetField("LONG"), feature.GetField("LAT"), feature.GetField("ALT"))
    geojson = point.ExportToJson()
    feature_collection.append(geojson)

    
#mais que cest chiant le printout des list en python, il met des ' partout, faut bricoler comme d'hab
print("[" + ', '.join(feature_collection) + "]")

dataSourceIn = None

