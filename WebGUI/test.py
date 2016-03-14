# -*- coding: utf-8 -*-
import cx_Oracle

ip='129.128.41.233'
port = 61234
sid = 'CRS'
con = cx_Oracle.makedsn(ip, port, sid);
db = cx_Oracle.connect('vfrunza/GenCortez741@localhost:61234/CRS')
print "hello"
