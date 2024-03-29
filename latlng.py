#!/usr/bin/python3

#https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

#./latlng 43.946831 4.011539 16 doit donner 33498 23843

import math
import sys


def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  print(xtile, ytile)
  
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  print("%.14f" % lat_deg, "%.14f" % lon_deg)

#print sys.argv[1]
deg2num(float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]))
#num2deg(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])) 
