#!/usr/bin/python

import cgitb
import cgi
import json
import math
import os.path

from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon

cgitb.enable()

def WGS84toGoogleBing(lon, lat):
    x = lon * 20037508.34 / 180.
    y = math.log(math.tan((90. + lat) * math.pi / 360.)) / (math.pi / 180.)
    y = y * 20037508.34 / 180.
    return [x, y]

def googleBingtoWGS84Mercator (x, y):
    lon = (x / 20037508.34) * 180
    lat = (y / 20037508.34) * 180

    lat = 180/math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return [lon, lat]

def getTileBoundary(x, y, z, globalBoundary):

    k = 20037508.34
    status = None

    x1 =( float( x )/2**(z-1) - 1)*k
    x2 =( float(x+1)/2**(z-1) - 1)*k

    y1=(1 - float(y+1)/ 2**(z-1))*k
    y2=(1 - float( y )/ 2**(z-1))*k

    # print globalBoundary

    polyTile = Polygon([[x1,y1], [x1, y2], [x2, y2], [x2, y1]])
    tileBoundary = globalBoundary.intersection(polyTile)
    
    if tileBoundary.is_empty:
        return
    
    if not isinstance(tileBoundary, Polygon):
        status = "Multipolygon"
    elif  len(tileBoundary.interiors) > 0:
        status = "Internals"
    else:
        status = "OK"
        
    return (status, tileBoundary)

params = cgi.FieldStorage()
strBoundary = params['boundary'].value
boundary = json.loads(strBoundary)

initGeometry = []
for p in boundary:
    initGeometry.append((p[0], p[1:]))

polyBoundary = MultiPolygon(initGeometry)

wrongPolygons = []

print "Content-Type: application/json"
print

for x in range(300, 320):
    for y in range(150, 170):
        res = getTileBoundary(x, y, 9, polyBoundary)
        if (res is not None) and (res[0] != 'OK'):
            wrongPolygons.append(res[1])
        
if len(wrongPolygons) > 0:
    wkts = [p.wkt for p in wrongPolygons]
    print json.dumps({'status': 'error', 'wrongRectangles': wkts})
else:
    f = open('boundary.txt', 'w')
    f.write(strBoundary)
    f.close()
    
    for x in range(300, 320):
        for y in range(150, 170):
            res = getTileBoundary(x, y, 9, polyBoundary)
            
            if res is not None:
                filename = "tiles/{0}_{1}_{2}.txt".format(x, y, 9)
                allCoords = []
                for p in res[1].exterior.coords:
                    allCoords.extend(googleBingtoWGS84Mercator(p[0], p[1]))
                
                coordsString = ','.join(map(str, allCoords))
                
                if  not os.path.exists(filename) or not open(filename, "r").read() == coordsString:
                    geomFile = open(filename, "w")
                    geomFile.write(coordsString)
                    geomFile.close()
                
    print json.dumps({'status': 'ok'})