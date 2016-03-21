#!/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, cgi, re
cgitb.enable()
import cx_Oracle

print "Content-type: text/html\n"
print ""
print ""
print "<html>"
print "<body>"


class NameNumberError(Exception):
	def __init__(self):
		pass

class FineError(Exception):
	def __init__(self):
		pass

class SINLengthError(Exception):
	def __init__(self):
		pass

class NoSINError(Exception):
	def __init__(self):
		pass

class NoSerialError(Exception):
	def __init__(self):
		pass

class SerialLengthError(Exception):
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

def ViolationSQL(sin, office, serial, place, vtype, description, date):

	max_ticketSQL = "SELECT MAX(ticket_no) FROM ticket"
	result = SendToOracle(max_ticketSQL, False)
	ticket_no = int(result[0][0]) + 1

	ticket_no = str(ticket_no)
	sin = "'"+str(sin.upper())+"'"
	office = "'"+str(office.upper())+"'"
	serial = "'"+str(serial.upper())+"'"
	place = "'"+str(place)+"'"
	vtype = "'"+str(vtype)+"'"
	description = "'"+str(description)+"'"
	date = "'"+str(date)+"'"

	TicketSQL = "INSERT INTO ticket VALUES("+ticket_no+", "+sin+", "+serial+", "+office+", "+vtype+", TO_DATE("+date+", 'yyyy/mm/dd'), "+place+", "+description+")"

	SendToOracle(TicketSQL, True)

def SerialValidation(serial):

	if len(str(serial)) != 15:
		raise SerialLengthError

	serial = "'"+str(serial)+"'"
	serial_SQL = "SELECT * FROM vehicle v WHERE UPPER(v.serial_no) = "+serial.upper()
	result = SendToOracle(serial_SQL, False)
	if result == []:
		raise NoSerialError

def SINValidation(sin):

	if len(str(sin)) != 15:
		raise SINLengthError

	sin = "'"+str(sin)+"'"
	sin_SQL = "SELECT * FROM people p WHERE UPPER(p.sin) = "+sin.upper()
	result = SendToOracle(sin_SQL, False)
	if result == []:
		raise NoSINError

try:
	form = cgi.FieldStorage()

	sin = str(form.getvalue("sin"))
	office = str(form.getvalue("office_no"))
	serial = str(form.getvalue("vehicle_id"))
	place = str(form.getvalue("place"))
	vtype = str(form.getvalue("vtype"))
	description = str(form.getvalue("description"))
	date = str(form.getvalue("s_date"))
	SerialValidation(serial)

	if sin == 'None':
		test_serial = "'"+str(serial.upper())+"'"
		result = SendToOracle("SELECT owner_id FROM owner o WHERE UPPER(o.vehicle_id) = "+test_serial.upper()+" AND is_primary_owner = 'y'", False)
		sin = result[0][0]
	else:
		SINValidation(sin)

	ViolationSQL(sin, office, serial, place, vtype, description, date)

except NameNumberError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Name</h2>
		<p>The name you entered had numbers in it. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except FineError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Fine</h2>
		<p>Please enter a fine with three digits before the ddecimal, and two digits after. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except SINLengthError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid SIN</h2>
		<p>A valid SIN is 15 digits long, with numbers only. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except NoSINError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>No SIN Found</h2>
		<p>This SIN number does not exist in the database. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except NoSerialError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>No Serial Number Found</h2>
		<p>This serial number does not exist in the database. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except SerialLengthError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Serial Number</h2>
		<p>A valid serial number is 15 digits long, with numbers only. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Database Error</h2>
		<p>An unexpected error occured. Please try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
	</paper-material>

</body>
</html>
	'''
