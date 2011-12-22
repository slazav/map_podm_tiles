#!/usr/bin/python

import cgitb
cgitb.enable()

print "Content-Type: application/json"
print

print open('boundary.txt', 'r').read()