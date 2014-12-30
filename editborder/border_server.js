// Super simple server to manage crop boundary file
var express = require('express'),
    cors = require('cors'),
    multer = require('multer'),
    fs = require('fs');

var app = express();

app.use(cors());
app.use(multer());

app.post('/save', function(req, res) {
    var geoJSON = req.body.border;
    fs.writeFile('./boundary.json', geoJSON);
    res.json('Success');
    console.log('boundary saved');
});

app.get('/get', function(req, res) {
    var geoJSON = fs.readFileSync('./boundary.json', {encoding: 'utf8'});
    res.json(JSON.parse(geoJSON));
})

app.listen(3001);
