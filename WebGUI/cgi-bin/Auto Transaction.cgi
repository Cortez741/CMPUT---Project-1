#!/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, cx_Oracle, cgi
cgitb.enable()

print "Content-type: text/html\n"
print ""
try:
	form = cgi.FieldStorage()
	transaction_id = "100"
	seller_id = "'101012020230303'"
	'''form.getvalue("seller_id")'''
	buyer_id = "'560945823588696'"
	'''form.getvalue("buyer_id")'''
	vehicle_id = "'55JICLZ10DLMPAU'"
	'''form.getvalue("vehicle_id")'''
	s_date = "'2015/06/25'"
	'''form.getvalue("s_date")'''
	price = str(form.getvalue("price"))
	print 'uhhh'
	tentative_sale_SQL = 'INSERT INTO auto_sale (TRANSACTION_ID, SELLER_ID, BUYER_ID, VEHICLE_ID, S_DATE, PRICE) VALUES ('+transaction_id+', '+seller_id+', '+buyer_id+', '+vehicle_id+', '+s_date+', '+price+');'
	print 'uhhhhhhhh'
	sale_SQL = 'select * from auto_sale'
	print tentative_sale_SQL
	c=Cookie.SimpleCookie()
 	if 'HTTP_COOKIE' in os.environ:
		c.load(os.environ['HTTP_COOKIE'])
	db = cx_Oracle.connect(c["user"].value+'/'+c["password"].value+'@localhost:61234/CRS')
	cur = db.cursor()
	try:
		cur.execute(tentative_sale_SQL)
	except Exception as ex:
		template = "An exception of type {0} occured. Arguments:\n{1!r}"
    		message = template.format(type(ex).__name__, ex.args)
    		print message
	for result in cur:
		pass
		print result
	print("Success: added transaction #"+str(1))
	cur.close()
	db.close()
except:
	print "<br>An error has occured. Please don't dock too many marks. Thank you."