#!/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, sys, platform
cgitb.enable()

print "Content-type: text/html"
print

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)
    try:
        data=c['raspberrypi'].value
        print "cookie data: "+data+"<br>"
	rerun = True
	if not 'LD_LIBRARY_PATH' in os.environ:
		os.environ['LD_LIBRARY_PATH'] = "/usr/local/stow/python3-cx_Oracle-5.2/lib/python3.4/dist-packages"
	elif "/usr/local/stow/python3-cx_Oracle-5.2/lib/python3.4/dist-packages" not in os.environ.get('LD_LIBRARY_PATH'):
		os.environ['LD_LIBRARY_PATH'] += "/usr/local/stow/python3-cx_Oracle-5.2/lib/python3.4/dist-packages"
	else:
		rerun = False
	if rerun:
		os.execve(os.path.realpath(__file__), sys.argv, os.environ)
	print os.environ.get('LD_LIBRARY_PATH')
	print sys.path
    except KeyError:
        print "The cookie was not set or has expired<br>"