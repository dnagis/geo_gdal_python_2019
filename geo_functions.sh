#!/usr/bin/bash

#Fonctions calcul geo pour aider le script recup_tiles et eviter de trop le bloater


#coord_to_bbox argument: coordonnées centrales (lat lng en wgs84 décimal) et taille souhaitée (distance 
#centre - bord), retourne un array avec NW et SE
#utilise proj (pkg proj-bin en debian)

coord_to_bbox () {
LAT=$1
LNG=$2
KM=$3

#echo "la fonction coord_to_bbox vient de recevoir $LAT $LNG $KM"

X=`echo $LAT , $LNG | sed 's/, //g' | cs2cs -d 0 EPSG:4326 EPSG:2154 | cut -f 1`
Y=`echo $LAT , $LNG | sed 's/, //g' | cs2cs -s -d 0 EPSG:4326 EPSG:2154 | cut -f 1`	

#echo "en lambert : $X $Y"

#Calculer des points NW et SE avec distances multiples de "KM" (Coordonnees Lambert sont des m)
XNW=$(($X-($KM*1000)))
YNW=$(($Y+($KM*1000)))
XSE=$(($X+($KM*1000)))
YSE=$(($Y-($KM*1000)))

#Avoir les coordonnées de ces deux points NW et SE en WGS84
NW=`echo "$XNW $YNW" | cs2cs -f %.6f EPSG:2154 EPSG:4326` 
SE=`echo "$XSE $YSE" | cs2cs -f %.6f EPSG:2154 EPSG:4326` 

lat0=`echo $NW | cut -f 1 -d ' '`
lng0=`echo $NW | cut -f 2 -d ' '`
latN=`echo $SE | cut -f 1 -d ' '`
lngN=`echo $SE | cut -f 2 -d ' '`

echo $lat0 $lng0 $latN $lngN

}
