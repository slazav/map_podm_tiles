// Script to test "crop_tile.js" utility
var fs = require('fs'),
    spawn = require('child_process').spawn;

var filenames = fs.readdirSync('../result/png_border');

var processFile = function() {
    if (!filenames.length) {
        return;
    }

    var filename = filenames.shift(),
        p = filename.match(/t(\d+)-(\d+).png/);

    if (p) {
        console.log('start', filename);
        var proc = spawn('node', ['crop_tile.js', 'boundary.json', p[1], p[2], 9, 1024]);
        proc.on('close', processFile);
        
        proc.stderr.on('data', function (data) {
              console.log('' + data);
        });

    } else {
        processFile();
    }

    //console.log(parsed);
}

processFile();
