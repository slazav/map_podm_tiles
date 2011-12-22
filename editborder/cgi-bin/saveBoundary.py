#!/usr/bin/python

import cgitb
import cgi
import json
cgitb.enable()

params = cgi.FieldStorage()

print "Content-Type: application/json"
# print "Content-Type: text/html"
print

boundary=params['boundary'].value
f = open('boundary.txt', 'w')
f.write(boundary)
f.close()

print json.dumps({status: 'ok'})