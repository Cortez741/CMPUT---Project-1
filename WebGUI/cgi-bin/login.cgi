#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb, Cookie, os, cgi
cgitb.enable()

form = cgi.FieldStorage()

import cx_Oracle

# create the cookie
c=Cookie.SimpleCookie()
variable = ""
value = ""
for key in form.keys():
        variable = str(key)
        value = str(form.getvalue(variable))
        # assign a value
	c[variable]=value
	# set the xpires time
	c[variable]['expires']=1*1*3*60*60

# print the header, starting with the cookie
print "Content-type: text/html\n"
print ""
print ""
print '''
<html>
<head>
    <title>Login - Error</title>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, minimum-scale=1.0, initial-scale=1.0, user-scalable=yes">

    <script src="../bower_components/webcomponentsjs/webcomponents-lite.js"></script>

    <link rel="import" href="../bower_components/iron-flex-layout/iron-flex-layout-classes.html">
    <link rel="import" href="../bower_components/iron-flex-layout/iron-flex-layout.html">
    <link rel="import" href="../bower_components/paper-styles/typography.html">
    <link rel="import" href="../bower_components/paper-button/paper-button.html">
    <link rel="import" href="../bower_components/paper-checkbox/paper-checkbox.html">
    <link rel="import" href="../bower_components/paper-dropdown-menu/paper-dropdown-menu.html">
    <link rel="import" href="../bower_components/paper-input/paper-input.html">
    <link rel="import" href="../bower_components/paper-item/paper-item.html">
    <link rel="import" href="../bower_components/paper-menu/paper-menu.html">
    <link rel="import" href="../bower_components/paper-spinner/paper-spinner.html">
    <link rel="import" href="../bower_components/paper-styles/color.html">
    <link rel="import" href="../bower_components/paper-styles/typography.html">
    <link rel="import" href="../bower_components/iron-form/iron-form.html">
    <link rel="import" href="../bower_components/paper-styles/demo-pages.html">
    <link rel="import" href="../bower_components/paper-button/paper-button.html">
    <link rel="import" href="../bower_components/paper-drawer-panel/paper-drawer-panel.html">
    <link rel="import" href="../bower_components/paper-styles/paper-styles.html">
    <link rel="import" href="../bower_components/paper-styles/demo-pages.html">
    <link rel="import" href="../bower_components/paper-header-panel/paper-header-panel.html">
    <link rel="import" href="../bower_components/paper-card/paper-card.html">

    <link rel="import" href="../bower_components/paper-dialog/paper-dialog.html">
    <link rel="import" href="../bower_components/paper-button/paper-button.html">
    <link rel="import" href="../bower_components/paper-dialog-scrollable/paper-dialog-scrollable.html">
    <link rel="import" href="../bower_components/paper-styles/color.html">
    <link rel="import" href="../bower_components/paper-styles/demo-pages.html">
    <link rel="import" href="../bower_components/paper-dropdown-menu/paper-dropdown-menu.html">
    <link rel="import" href="../bower_components/paper-menu/paper-menu.html">
    <link rel="import" href="../bower_components/paper-item/paper-item.html">


    <style>
	html, body { margin: 0; padding: 0; }
	.centeredDiv { margin-right: auto; margin-left: auto; width: 100%;}
        a {
        color: black;
        text-decoration: none; /* no underline */
        }
    </style>
    <style is="custom-style">
      paper-header-panel {
        float: left;
        width: 240px;
        height: 240px;
        @apply(--shadow-elevation-2dp);
      }
      .paper-header {
        height: 60px;
        font-size: 16px;
        line-height: 60px;
        padding: 0 10px;
        color: white;
        transition: height 0.2s;
      }
      .paper-header.tall {
        height: 120px;
      }
      .paper-header.medium-tall {
        height: 100px;
        line-height: 50px;
      }
      .content {
        height: 2000px;
      }
      .cover {
        margin: 60px;
      }
      .blue .paper-header {
        background-color: var(--paper-light-blue-500);
      }
      .red .paper-header {
        background-color: var(--paper-red-500);
      }
      .orange .paper-header {
        background-color: var(--paper-amber-500);
      }
      .green .paper-header {
        background-color: var(--paper-green-500);
      }
      .cyan .paper-header {
        background-color: var(--paper-cyan-500);
      }
      .lime .paper-header {
        background-color: var(--paper-lime-500);
      }
      .pink .paper-header {
        background-color: var(--paper-pink-a200);
      }
      /* TODO: replace these with background: linear-gradient(white, var(...))
       when custom properties allow it */
      .blue .content {
        background: linear-gradient(white, #b3e5fc);
      }
      .red .content {
        background: linear-gradient(white, #ffcdd2);
      }
      .orange .content {
        background: linear-gradient(white, #ffecb3);
      }
      .green .content {
        background: linear-gradient(white, #c8e6c9);
      }
      .cyan .content {
        background: linear-gradient(white, #b2ebf2);
      }
      .lime .content {
        background: linear-gradient(white, #f0f4c3);
      }
      .pink .content {
        background: linear-gradient(white, #f8bbd0);
      }

      <style>
         .container {
           @apply(--layout-horizontal);
           @apply(--layout-center-justified);
         }
       </style>
 </head>
	<body style="margin-left: -242px; padding-left: 50%;">
'''
try:
	db = cx_Oracle.connect(form["user"].value+'/'+form["password"].value+'@localhost:61234/CRS')
	print '''	    <script>
				window.location.href = "../index.php"
			    </script>'''
except:
	print '''
    <paper-card image="/UAlberta.png">
		<div class="card-content">
			<p>Invalid login information. Please go back and try again.</p>
            		<a href="../index.html"><paper-button raised>Back to Login</paper-button></a>
		</div>
	</paper-card>

	</body>
</html>
'''
