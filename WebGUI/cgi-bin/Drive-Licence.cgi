#!/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, cgi, re, string
cgitb.enable()
import cx_Oracle

print "Content-type: text/html\n"
print ""
print ""

class SINLengthError(Exception):
	def __init__(self):
		pass

class SINError(Exception):
	def __init__(self):
		pass

class LicenceError(Exception):
	def __init__(self):
		pass

class LicenceLengthError(Exception):
	def __init__(self):
		pass

class LicenceExistsError(Exception):
	def __init__(self):
		pass

class IncompleteFormError(Exception):
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
	if isQuery==True:
		try:
			f_image = open('../uploads/photo.jpg','rb')
			image = f_image.read()
			blobvar = cur.var(cx_Oracle.BLOB)
			blobvar.setvalue(0, image)
			cur.setinputsizes(imageblob=cx_Oracle.BLOB)
			sql = string.replace(sql, "NULL",":imageblob")
			cur.execute(sql, imageblob = blobvar)
			f_image.close()
			os.remove('../uploads/photo.jpg')
		except:
			cur.execute(sql)
	else:
		cur.execute(sql)
	db.commit()
	if not isQuery:
		result = cur.fetchall()
		cur.close()
		db.close()
		return result
	cur.close()
	db.close()

def SINValidation(sin):

	if len(str(sin)) != 15:
		raise SINLengthError

	sin = "'"+str(sin)+"'"

	sin_SQL = "SELECT * FROM people p WHERE UPPER(p.sin) = "+sin.upper()
	result = SendToOracle(sin_SQL, False)

	if result == []:
		person_state = 1

	if result != []:
		person_state = 2

	sin_SQL = "SELECT * FROM drive_licence l WHERE UPPER(l.sin) = "+sin.upper()
	result = SendToOracle(sin_SQL, False)

	if result != []:
		person_state = 3

	return person_state

def LicenceValidation(licence_no):

	if len(str(licence_no)) != 15:
		raise LicenceLengthError

	licence_no = "'"+str(licence_no)+"'"
	sin_SQL = "SELECT * FROM drive_licence d WHERE UPPER(d.licence_no) = "+licence_no.upper()
	result = SendToOracle(sin_SQL, False)
	if result != []:
		raise LicenceExistsError

def PersonSQL(sin, name, height, weight, eye_color, hair_color, addr, gender, bday):
	sin = "'"+sin.upper()+"'"
	name = "'"+name+"'"
	height = "'"+height+"'"
	weight = "'"+weight+"'"
	eye_color = "'"+eye_color+"'"
	hair_color = "'"+hair_color+"'"
	addr = "'"+addr+"'"
	gender = "'"+gender.lower()+"'"
	bday = "'"+bday+"'"

	person_SQL = "INSERT INTO people VALUES ("+sin+",  "+name+", "+height+", "+weight+", "+eye_color+", "+hair_color+", "+addr+", "+gender+", TO_DATE("+bday+",'YYYY-MM-DD'))"
	result = SendToOracle(person_SQL, True)

def LicenceSQL(licence_no, sin, drive_class, issuing_date, expiring_date, driving_cond):
	licence_no = "'"+licence_no.upper()+"'"
	sin = "'"+sin.upper()+"'"
	drive_class = "'"+drive_class+"'"
	issuing_date = "'"+issuing_date+"'"
	expiring_date = "'"+expiring_date+"'"
	driving_cond = "'"+driving_cond+"'"

	licence_SQL = "INSERT INTO drive_licence VALUES ("+licence_no+",  "+sin+", "+drive_class+", NULL, TO_DATE("+issuing_date+",'YYYY-MM-DD'), TO_DATE("+expiring_date+",'YYYY-MM-DD'))"
	result = SendToOracle(licence_SQL, True)
try:
	form = cgi.FieldStorage()

	sin = str(form.getvalue("sin"))
	name = str(form.getvalue("name"))
	height = str(form.getvalue("height"))
	weight = str(form.getvalue("weight"))
	eye_color = str(form.getvalue("eye_color"))
	hair_color = str(form.getvalue("hair_color"))
	addr = str(form.getvalue("addr"))
	gender = str(form.getvalue("gender"))
	bday = str(form.getvalue("bday"))

	licence_no = str(form.getvalue("licence_no"))
	drive_class = str(form.getvalue("class"))
	issuing_date = str(form.getvalue("issuing_date"))
	expiring_date = str(form.getvalue("expiring_date"))
	driving_cond = str(form.getvalue("driving_cond"))

	LicenceValidation(licence_no)
	sin_state = SINValidation(sin)

	if name == 'None' and sin_state == 1:
		raise IncompleteFormError

	if name != 'None' and sin_state == 1:
		PersonSQL(sin, name, height, weight, eye_color, hair_color, addr, gender, bday)
		LicenceSQL(licence_no, sin, drive_class, issuing_date, expiring_date, driving_cond)

	if sin_state == 2:
		LicenceSQL(licence_no, sin, drive_class, issuing_date, expiring_date, driving_cond)

	if sin_state == 3:
		raise LicenceError

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

except SINError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>SIN Found</h2>
		<p>This SIN number already exists in the database. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except LicenceError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Licence Number Found</h2>
		<p>This person already has a licence. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except LicenceExistsError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Licence Number Found</h2>
		<p>This Licence number already exists in the database. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except LicenceLengthError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Licence Number</h2>
		<p>A valid Licence number is 15 digits long. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''

except IncompleteFormError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Incomplete Form</h2>
		<p>This form was incomplete. Please Try again.</p>
	</paper-material>
</body>
</html>
	'''
