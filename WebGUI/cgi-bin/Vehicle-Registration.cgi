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


def FormSQL(serial_no, maker, model, year, color, type_id, owner_id, sowner_id):
	serial_no = "'"+serial_no+"'"
	maker = "'"+maker+"'"
	model = "'"+model+"'"
	color = "'"+color+"'"
	owner_id = "'"+owner_id+"'"
	sowner_id = "'"+sowner_id+"'"
	owner_SQL = "SELECT * FROM people p WHERE UPPER(p.sin) = "+owner_id.upper()
	sowner_SQL = "SELECT * FROM people p WHERE UPPER(p.sin) = "+sowner_id.upper()
	vehicle_SQL = "SELECT * FROM vehicle v WHERE UPPER(v.serial_no) = "+serial_no.upper()
	result = SendToOracle(vehicle_SQL, False)
	if result != []:
		print "Vehicle is already registered; please try again."
		raise NoResultsError
	result = SendToOracle(owner_SQL, False)
	if result == []:
		print '''<img id="addingowner" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" onload="var a = document.getElementById('basicdiv'); var b= document.getElementById('adduserdiv'); a.style.visibility='hidden'; a.style.position='absolute'; b.style.visibility='visible'; b.style.position='relative'"\>'''
		raise Exception
	result = SendToOracle(sowner_SQL, False)
	if sowner_id != "''" and result == []:
		print '''<img id="addingsowner" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" onload="var a = document.getElementById('basicdiv'); var b= document.getElementById('adduserdiv'); a.style.visibility='hidden'; a.style.position='absolute'; b.style.visibility='visible'; b.style.position='relative'"\>'''
		raise Exception
	addvehicle_SQL = "INSERT INTO vehicle v VALUES ("+serial_no+","+maker+", "+model+", "+year+", "+color+", "+type_id+")"
	result = SendToOracle(addvehicle_SQL, True)
	addowner_SQL = "INSERT INTO owner v VALUES ("+owner_id+","+serial_no+", 'y')"
	result = SendToOracle(addowner_SQL, True)
	addsowner_SQL = "INSERT INTO owner v VALUES ("+sowner_id+","+serial_no+", 'n')"
	result = SendToOracle(addsowner_SQL, True)
	print "success"

try:
	form = cgi.FieldStorage()
	serial_no = str(form.getvalue("serial_no"))
	maker = str(form.getvalue("maker"))
	model = str(form.getvalue("model"))
	year = str(form.getvalue("year"))
	color = str(form.getvalue("color"))
	type_id = str(form.getvalue("type_id"))
	owner_id = str(form.getvalue("owner_id"))
	sowner_id = str(form.getvalue("sowner_id"))
	FormSQL(serial_no, maker, model, year, color, type_id, owner_id, sowner_id)
except:
	pass
