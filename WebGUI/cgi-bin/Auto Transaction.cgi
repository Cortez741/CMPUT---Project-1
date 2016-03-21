#!/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, cx_Oracle, cgi, re
cgitb.enable()

print "Content-type: text/html\n"
print ""
print ""
print "<html>"
print "<body>"

class NoResultsError(Exception):
	def __init__(self):
		pass

def SendToOracle(sql, isQuery):
	c = Cookie.SimpleCookie()
	if 'HTTP_COOKIE' in os.environ:
		c.load(os.environ['HTTP_COOKIE'])
	try:
		db = cx_Oracle.connect(c["user"].value+'/'+c["password"].value+'@localhost:61234/CRS')
	except:
	    print '''
	    <paper-material elevation="2">
	    <div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
	        <h2>Login Timeout</h2>
	        <p>Please go back to the login page and login again.</p>
	        <br>
	        <a href="http://vfrunza.ca"><paper-button raised>Back</paper-button></a>
	    </paper-material>
	</body>
	</html>
	'''
	cur = db.cursor()
	cur.execute(sql)
	db.commit()
	if not isQuery:
		result = cur.fetchall()
		cur.close()
		db.close()
		return result
	cur.close()
	db.close()

def FormSQL(transaction, seller, buyer, vehicle, price, date, primowner, owners):
	seller = "'"+seller+"'"
	buyer = "'"+buyer+"'"
	vehicle = "'"+vehicle+"'"
	date = "'"+date+"'"
	primowner = "'"+primowner+"'"
	oldowners = re.sub(r'\s+', '', owners)
	owners = oldowners.split(",")

	sellerexists_SQL = "SELECT * FROM people p, owner o, vehicle v WHERE p.sin = o.owner_id AND o.vehicle_id = v.serial_no AND UPPER(v.serial_no) = "+vehicle.upper()+" AND UPPER(p.sin) = "+seller.upper()
	result = SendToOracle(sellerexists_SQL, False)

	if result == []:
		print "The seller is not an owner of the vehicle; please try again."
		raise NoResultsError

	vehicleexists_SQL = "SELECT * FROM vehicle v WHERE UPPER(v.serial_no) = "+vehicle.upper()
	result = SendToOracle(vehicleexists_SQL, False)

	if result == []:
		print "The vehicle does not exist in the database; please try again."
		raise NoResultsError

	seller_SQL = "SELECT * FROM people p WHERE p.sin = "+seller
	buyer_SQL = "SELECT * FROM people p WHERE p.sin = "+buyer
	vehicle_SQL = "SELECT * FROM vehicle v WHERE v.serial_no = "+vehicle
	owners_SQL = "DELETE FROM owner o WHERE o.vehicle_id = "+vehicle
	primowner_SQL = "INSERT INTO owner VALUES ("+primowner+", "+vehicle+", 'y')"
	secondaryowner_SQL = []

	for secondaryowner in owners:
		secondaryowner_SQL.append("INSERT INTO owner VALUES ('"+secondaryowner+"', "+vehicle.upper()+", 'n')")

	transaction_SQL = "SELECT MAX( transaction_id ) FROM auto_sale"
	result = int(SendToOracle(transaction_SQL, False)[0][0])+1
	result = SendToOracle(seller_SQL, False)

	if result == []:
		print "Seller ID does not exist; please try again."
		raise NoResultsError

	result = SendToOracle(vehicle_SQL, False)

	if result == []:
		print "Serial Number does not exist; please try again."
		raise NoResultsError

	result = SendToOracle(buyer_SQL, False)

	if result == []:
		print '''<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" onload="var a = document.getElementById('basicdiv'); var b= document.getElementById('adduserdiv'); a.style.visibility='hidden'; a.style.position='absolute'; b.style.visibility='visible'; b.style.position='relative'"\>'''

	result = SendToOracle(owners_SQL, True)
	result = SendToOracle(primowner_SQL, True)

	for owner_SQL in secondaryowner_SQL:
		SendToOracle(owner_SQL, True)
try:

	form = cgi.FieldStorage()
	seller_id = str(form.getvalue("seller_id"))
	buyer_id = str(form.getvalue("buyer_id"))
	vehicle_id = str(form.getvalue("vehicle_id"))
	price = str(form.getvalue("price"))
	s_date = str(form.getvalue("s_date"))
	prim_owner = str(form.getvalue("prim_owner"))
	owners = str(form.getvalue("owners"))

	FormSQL(100, seller_id, buyer_id, vehicle_id, price, s_date, prim_owner, owners)
except:
	pass
