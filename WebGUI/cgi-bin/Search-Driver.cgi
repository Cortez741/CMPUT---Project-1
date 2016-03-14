#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, cgi, string
cgitb.enable()

import cx_Oracle

print "Content-type: text/html\n"
print " "

def LicenceSQL(licence_no):
    licence_no = licence_no.lower()
    licence_SQL = "SELECT * FROM drive_licence WHERE licence_no="+str(licence_no)+";"
    return licence_SQL

def NameSQL(name):
    name = name.lower()
    name_SQL = "SELECT * FROM people WHERE name="+name+";"
    return name_SQL

try:
    form = cgi.FieldStorage()

    licence_no = form.getvalue("licence_no")
    name = form.getvalue("name")
    print name
    print licence_no

    if name == None:
        result = LicenceSQL(licence_no)
        print result

    if licence_no == None:
        result = NameSQL(name)
        print result

except:
    print "fail"


#copy form variables into python ones
