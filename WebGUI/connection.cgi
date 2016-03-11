#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os
cgitb.enable()

# create the cookie
c=Cookie.SimpleCookie()
# assign a value
c['raspberrypi']='Hello world'
# set the xpires time
c['raspberrypi']['expires']=1*1*3*60*60

# print the header, starting with the cookie
print c
print "Content-type: text/html\n"
print ""
print ""
print '''
<html>
	<head>
		<script>
			window.location.href = "index.php";
		</script>
	</head>
</html>
'''