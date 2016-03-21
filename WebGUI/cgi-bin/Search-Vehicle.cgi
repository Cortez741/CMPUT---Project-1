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

class NoSerialError(Exception):
	def __init__(self):
		pass

class NoResultsError(Exception):
	def __init__(self):
		pass

def PrintResult1(result):
	print '''<table class="table">'''
	print '''
	<tr>
		<th>Transaction ID</th>
		<th>Seller</th>
		<th>Buyer</th>
		<th>Vehicle</th>
		<th>Date</th>
		<th>Price</th>
	</tr>
	'''
	for row in result:
		print "<tr>"
		for item in row:
			print "<td>"+str(item)+"</td>"
		print "</tr>"
	print "</table>"

def PrintResult2(result):
	print '''<table class="table">'''
	print '''
	<tr>
		<th>Ticket Number</th>
		<th>Violator Number</th>
		<th>Vehicle ID</th>
		<th>Office Number</th>
		<th>Violation Type</th>
		<th>Violation Date</th>
		<th>Place</th>
		<th>Description</th>
		<th>Fine</th>
	</tr>
	'''
	for row in result:
		print "<tr>"
		for item in row:
			print "<td>"+str(item)+"</td>"
		print "</tr>"
	print "</table>"

def PrintResult3(result):
	print '''<table class="table">'''
	print '''
	<tr>
		<th>Number of Transactions</th>
		<th>Average Price</th>
		<th>Number of Violations</th>
	</tr>
	'''
	print "<tr>"
	for item in result:
		print "<td><p>"+str(item)+"</p></td>"

	print "</tr>"
	print "</table>"

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

def SerialValidation(serial):
	if len(str(serial)) != 15:
		raise LengthError

	serial = "'"+str(serial)+"'"
	serial_SQL = "SELECT * FROM vehicle v WHERE UPPER(v.serial_no) = "+serial.upper()
	result = SendToOracle(serial_SQL)
	if result == []:
		raise NoSerialError

def SerialSQL1(serial):
	serial = "'"+serial+"'"
	serial_SQL = "SELECT * FROM auto_sale a WHERE UPPER(a.vehicle_id) = "+serial.upper()
	result = SendToOracle(serial_SQL)
	if result == []:
		result = [['None', 'None', 'None', 'None', 'None', 'None']]
	PrintResult1(result)

def SerialSQL2(serial):
	serial = "'"+serial+"'"
	serial_SQL = "SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions, tt.fine FROM vehicle v, ticket t, ticket_type tt WHERE UPPER(v.serial_no) = "+serial.upper()+" AND v.serial_no = t.vehicle_id AND t.vtype=tt.vtype"
	result = SendToOracle(serial_SQL)

	if result == []:
		result = [['None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None']]
	PrintResult2(result)

def SerialSQL3(serial):
	serial_stats = []
	serial = "'"+serial+"'"
	serial_SQL = "SELECT COUNT(a.vehicle_id) FROM auto_sale a WHERE UPPER(a.vehicle_id) = "+serial.upper()
	result = SendToOracle(serial_SQL)

	if result == None:
		result = '0'
		serial_stats.append(result)
	else:
		serial_stats.append(result[0][0])

	serial_SQL = "SELECT AVG(a.price) FROM auto_sale a WHERE UPPER(a.vehicle_id) = "+serial.upper()+" GROUP BY a.price"
	result = SendToOracle(serial_SQL)

	if result == []:
		result = 'None'
		serial_stats.append(result)
	else:
		serial_stats.append(result[0][0])

	serial_SQL = "SELECT COUNT(t.ticket_no) FROM vehicle v, ticket t WHERE UPPER(v.serial_no) = "+serial.upper()+" AND v.serial_no = t.vehicle_id"
	result = SendToOracle(serial_SQL)

	if result == None:
		result = '0'
		serial_stats.append(result)
	else:
		serial_stats.append(result[0][0])

	PrintResult3(serial_stats)

try:
	form = cgi.FieldStorage()
	serial = form.getvalue("serial").upper()

	SerialValidation(serial)
	SerialSQL3(serial)
	SerialSQL1(serial)
	SerialSQL2(serial)
	print '''
		<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="../js/bootstrap.min.js"></script>
		</body>
		</html>
		'''

except NoSerialError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>No Serial Number Exists</h2>
		<p>That serial number does not exisit. Please try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
	</paper-material>
</body>
</html>
	'''

except LengthError:
	print '''
	<paper-material elevation="2">
	<div style="padding-top: 20px; padding-bottom: 20px; padding-right: 20px; padding-left: 20px;">
		<h2>Invalid Serial Number</h2>
		<p>The Serial number you entered was not 15 digits long. Please type one 15 digit number without spaces or dashes. Please Try again.</p>
		<br>
		<a href="http://vfrunza.ca/index.php?page=Search"><paper-button raised>Back</paper-button></a>
	</paper-material>
</body>
</html>
	'''
#except:
	#print "failed"
