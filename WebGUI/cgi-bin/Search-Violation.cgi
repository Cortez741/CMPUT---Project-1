#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, cgi, string
cgitb.enable()

import cx_Oracle

print "Content-type: text/html\n"
print " "
print '''
<html>

<head>
	<title>Registry - Home</title>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<meta name="viewport" content="width=device-width, minimum-scale=1.0, initial-scale=1.0, user-scalable=yes">
	<script src="../bower_components/webcomponentsjs/webcomponents-lite.js"></script>
	<link rel="import" href="../bower_components/iron-flex-layout/iron-flex-layout-classes.html">
	<link rel="import" href="../bower_components/iron-flex-layout/iron-flex-layout.html">
	<link rel="import" href="../bower_components/iron-form/iron-form.html">
	<link rel="import" href="../bower_components/paper-button/paper-button.html">
	<link rel="import" href="../bower_components/paper-checkbox/paper-checkbox.html">
	<link rel="import" href="../bower_components/paper-dropdown-menu/paper-dropdown-menu.html">
	<link rel="import" href="../bower_components/paper-input/paper-input.html">
	<link rel="import" href="../bower_components/paper-item/paper-item.html">
	<link rel="import" href="../bower_components/paper-menu/paper-menu.html">
	<link rel="import" href="../bower_components/paper-spinner/paper-spinner.html">
	<link rel="import" href="../bower_components/paper-styles/color.html">
	<link rel="import" href="../bower_components/paper-styles/typography.html">
	<link rel="import" href="../bower_components/paper-styles/demo-pages.html">
	<link rel="import" href="../bower_components/paper-styles/paper-styles.html">
	<link rel="import" href="../bower_components/paper-button/paper-button.html">
	<link rel="import" href="../bower_components/paper-drawer-panel/paper-drawer-panel.html">
	<link rel="import" href="../bower_components/paper-styles/paper-styles.html">
	<link rel="import" href="../bower_components/paper-styles/demo-pages.html">
	<link rel="import" href="../bower_components/paper-header-panel/paper-header-panel.html">
	<link rel="import" href="../bower_components/paper-card/paper-card.html">
	<link rel="import" href="../bower_components/paper-dialog/paper-dialog.html">
	<link rel="import" href="../bower_components/paper-dialog-scrollable/paper-dialog-scrollable.html">
	<link rel="import" href="../bower_components/neon-animation/neon-animations.html">
	<link rel="import" href="../bower_components/neon-animation/animations/scale-up-animation.html">
	<link rel="import" href="../bower_components/neon-animation/animations/fade-out-animation.html">
	<link href="../css/bootstrap.min.css" rel="stylesheet">
	<link rel="stylesheet" href="../bower_components/paper-styles/demo.css">

  <style is="custom-style">
	section {
	  -webkit-tap-highlight-color: rgba(0,0,0,0);
	}

	section > paper-button {
	  background-color: var(--google-grey-300);
	  padding: 5px;
	}
	section > paper-button:hover {
	  background-color: var(--paper-light-blue-200);
	  padding: 5px;
	}
	paper-dialog.colored {
	  border: 2px solid;
	  border-color: var(--paper-green-500);
	  background-color: var(--paper-light-green-50);
	  color: var(--paper-green-500);
	}
	paper-dialog.size-position {
	  position: fixed;
	  top: 16px;
	  right: 16px;
	  width: 300px;
	  height: 300px;
	  overflow: auto;
	}
  </style>

</head>

<body>
	'''

class LengthError(Exception):
	def __init__(self):
		pass

class NoSINError(Exception):
	def __init__(self):
		pass

class NoLicenceError(Exception):
	def __init__(self):
		pass

class NoResultsError(Exception):
	def __init__(self):
		pass

def SendToOracle(sql):
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
	result = cur.fetchall()
	cur.close()
	db.close()
	return result

def PrintResults(result):
	print '''<table class="table">'''
	print '''
	<tr>
		<th>Ticket Number</th>
		<th>Violator ID</th>
		<th>Vehicle ID</th>
		<th>Office Number</th>
		<th>Violation Type</th>
		<th>Place</th>
		<th>Description of Violation</th>
		<th>Fine</th>
	</tr>
	'''
	for row in result:
		print "<tr>"
		for item in row:
			print "<td>"+str(item)+"</td>"
		print "</tr>"
	print "</table>"
	print '''<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>'''

	print '''
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="../js/bootstrap.min.js"></script>
		</body>
		</html>
		'''

def SinSQL(sin):
	sin = "'"+str(sin)+"'"
	sin_SQL = "SELECT ticket_no, violator_no, vehicle_id, office_no, f.vtype, place, descriptions, fine FROM ticket t, ticket_type f, drive_licence d WHERE UPPER(d.sin) = "+sin.upper()+" AND d.sin = t.violator_no AND t.vtype = f.vtype"
	return sin_SQL

def LicenceSQL(licence_no):
	licence_no = "'"+str(licence_no)+"'"
	licence_SQL = "SELECT ticket_no, violator_no, vehicle_id, office_no, f.vtype, place, descriptions, fine FROM ticket t, ticket_type f, drive_licence d WHERE UPPER(d.licence_no) = "+licence_no.upper()+" AND d.sin = t.violator_no AND t.vtype = f.vtype"
	return licence_SQL

def LicenceValidation(licence_no):
	test_int = int(licence_no)
	if len(str(licence_no)) != 15:
		raise LengthError
	licence_no = "'"+str(licence_no)+"'"
	sin_SQL = "SELECT * FROM drive_licence d WHERE UPPER(d.licence_no) = "+licence_no.upper()
	result = SendToOracle(sin_SQL)
	if result == []:
		raise NoLicenceError

def SINValidation(sin):
	test_int = int(sin)
	if len(str(sin)) != 15:
		raise LengthError
	sin = "'"+str(sin)+"'"
	sin_SQL = "SELECT * FROM people WHERE UPPER(people.sin) = "+sin.upper()
	result = SendToOracle(sin_SQL)
	if result == []:
		raise NoSINError

try:
	form = cgi.FieldStorage()
	sin = form.getvalue("violation_sin")
	licence_no = form.getvalue("licence_no")

	if sin == None:
		LicenceValidation(licence_no)
		licence_SQL = LicenceSQL(licence_no)
		result = SendToOracle(licence_SQL)
		if result == []:
			raise NoResultsError
		PrintResults(result)

	if licence_no == None:
		SINValidation(sin)
		sin_SQL = SinSQL(sin)
		result = SendToOracle(sin_SQL)
		if result == []:
			raise NoResultsError
		PrintResults(result)

except LengthError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Input</h2>
		<p>The inputs you entered was not 15 characters long. Please type one 15 character long string. Please Try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
	</paper-material>
</body>
</html>
	'''

except NoResultsError:
    print '''
    <paper-material elevation="2">
    <div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
        <h2>No Results</h2>
        <p>Your search returned no results.</p>
        <br>
        <a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
    </paper-material>
</body>
</html>
    '''

except NoSINError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>No SIN Exisits</h2>
		<p>The SIN you entered does not exist in this database, please try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
	</paper-material>
</body>
</html>
	'''

except NoLicenceError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>No Licence Number Exisits</h2>
		<p>The Licence Number you entered does not exist in this database, please try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
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
