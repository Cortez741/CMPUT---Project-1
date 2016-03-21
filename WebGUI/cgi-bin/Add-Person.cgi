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

class NameNumberError(Exception):
	def __init__(self):
		pass

class HeightError(Exception):
	def __init__(self):
		pass

class LengthError(Exception):
	def __init__(self):
		pass

class NoSerialError(Exception):
	def __init__(self):
		pass

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

def PersonValidate(name, height, weight):
	if not re.match(r'[0-9]*\.[0-9]{2}', height):
		raise HeightError
	if not re.match(r'[0-9]*\.[0-9]{2}', weight):
		raise WeightError

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
	PersonValidate(name, height, weight)
	addperson_SQL = "INSERT INTO people VALUES ('"+sin+"', '"+name+"',"+height+","+weight+",'"+eye_color+"','"+hair_color+"','"+addr+"','"+gender+"',TO_DATE('"+bday+"','YYYY-MM-DD'))"
	result = SendToOracle(addperson_SQL, True)
	print "success"
except NameNumberError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Name</h2>
		<p>The name you entered had numbers in it. Please Try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Add-Person"><paper-button raised>Back</paper-button></a>
	</paper-material>
</body>
</html>
	'''
except HeightError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Height</h2>
		<p>Height must be a decimal number with 3 digits before the decimal and two after. Please try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Add-Person"><paper-button raised>Back</paper-button></a>
	</paper-material>
</body>
</html>
	'''
except:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Error adding user</h2>
		<p>There was a problem with your submission. Please try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Add-Person"><paper-button raised>Back</paper-button></a>
	</paper-material>
</body>
</html>
	'''
