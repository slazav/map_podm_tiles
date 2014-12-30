// Syntax:
//   node crop_tile.js <boundary.json> <input.png> <output.png> <x> <y> <z> <internalZoom>
// 
// boundary.json is GeoJSON file with one or more Polygon features.
// All polygons are treated as components of boundary's multipolygon.
//
// x,y,z are coordinates of top-left image corner (OSM-style tile grid)
// 
// pixelZoom describes pixel size: pixel size is 1/256 of tile size at corresponding zoom.
// Used to crop images other then 256x256

var fs = require('fs'),
    Canvas = require('canvas'),
    proj4 = require('proj4');

var convertGeom = function(geoJSON, x, y, z, tileZ){
    var proj = proj4('EPSG:3857'),
        coords = [],
        w = proj.forward([180, 0])[0] - proj.forward([-180, 0])[0],
        tileSize = w / Math.pow(2, z),
        mInPixel = tileSize / Math.pow(2, tileZ - z + 8),
        mercX = x * tileSize - w/2,
        mercY = w/2 - y * tileSize;

    for (var f = 0; f < geoJSON.features.length; f++) {
        var fc = geoJSON.features[f].geometry.coordinates[0],
            rcoords = [];
        for (var p = 0; p < fc.length; p++) {
            var mc = proj.forward([fc[p][0], fc[p][1]]);
            rcoords.push([(mc[0] - mercX)/mInPixel, (mercY - mc[1])/mInPixel]);
        }
        coords.push(rcoords);
    }
    return coords;
}

var args = process.argv.slice(2);

var x = parseInt(args[3]),
    y = parseInt(args[4]),
    z = parseInt(args[5]),
    tileZ = parseInt(args[6]),
    inFilename = args[1],
    outFilename = args[2],
    img = new Canvas.Image(),
    geoJSON = JSON.parse(fs.readFileSync(args[0], 'utf8')),
    coords = convertGeom(geoJSON, x, y, z, tileZ);

img.onload = function() {
    var canvas = new Canvas(img.width, img.height),
        ctx = canvas.getContext('2d'),
        pattern = ctx.createPattern(img, "repeat");
    
    ctx.beginPath();
    for (var r = 0; r < coords.length; r++) {
        ctx.moveTo(coords[r][0][0], coords[r][0][1]);
        for (var p = 1; p < coords[r].length; p++) {
            ctx.lineTo(coords[r][p][0], coords[r][p][1]);
        }
    }
    ctx.clip();

    ctx.beginPath();
    ctx.rect(0, 0, img.width, img.height);
    ctx.fillStyle = pattern;
    ctx.fill();

    var out = fs.createWriteStream(outFilename),
        stream = canvas.createPNGStream();

    stream.on('data', function(chunk){
        out.write(chunk);
    });
}

img.onerror = function(e) {
    console.log(inFilename);
    console.log(e);
}

img.src = inFilename;
