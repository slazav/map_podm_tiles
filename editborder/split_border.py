from shapely.geometry import Polygon
# from pyproj import Proj
import json
import sys
import math

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

    x1 =( float( x )/2**(z-1) - 1)*k
    x2 =( float(x+1)/2**(z-1) - 1)*k

    y1=(1 - float(y+1)/ 2**(z-1))*k
    y2=(1 - float( y )/ 2**(z-1))*k

    polyTile = Polygon([[x1,y1], [x1, y2], [x2, y2], [x2, y1]]);
    # print polyTile.wkt
    # print poly1.wkt
    tileBoundary = globalBoundary.intersection(polyTile)
    
    if tileBoundary.is_empty:
        return
    
    if not isinstance(tileBoundary, Polygon):
        print "Not polygon: {} {} {}".format(x, y, z)
        print tileBoundary.wkt
    elif  len(tileBoundary.interiors) > 0:
        print "Has interiors: {} {} {}".format(x, y, z)
        print tileBoundary.wkt
    else:
        print "OK: {} {} {}".format(x, y, z)
        geomFile = open("tiles/{}_{}_{}.txt".format(x, y, z), "w")
        allCoords = []
        for p in tileBoundary.exterior.coords:
            allCoords.extend(googleBingtoWGS84Mercator(p[0], p[1]))
        geomFile.write(','.join(map(str, allCoords)))
        geomFile.close()

# x = float(sys.argv[1])
# y = float(sys.argv[2])
# z = float(sys.argv[3])

file = open('cgi-bin/boundary.txt', 'r');
boundary = json.loads(file.read())
file.close()
polyBoundary = Polygon(boundary[0], boundary[1:])

for x in range(300, 320):
    for y in range(150, 170):
        getTileBoundary(x, y, 9, polyBoundary)

# getTileBoundary(x, y, z)