<!doctype html>
<!--
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
Code distributed by Google as part of the polymer project is also
subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt
-->
<html>
<head>
    <title>Registry - Home</title>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, minimum-scale=1.0, initial-scale=1.0, user-scalable=yes">

    <script src="bower_components/webcomponentsjs/webcomponents-lite.js"></script>

    <link rel="import" href="bower_components/iron-flex-layout/iron-flex-layout.html">
    <link rel="import" href="bower_components/paper-styles/typography.html">
    <link rel="import" href="bower_components/paper-button/paper-button.html">
    <link rel="import" href="bower_components/paper-checkbox/paper-checkbox.html">
    <link rel="import" href="bower_components/paper-dropdown-menu/paper-dropdown-menu.html">
    <link rel="import" href="bower_components/paper-input/paper-input.html">
    <link rel="import" href="bower_components/paper-item/paper-item.html">
    <link rel="import" href="bower_components/paper-menu/paper-menu.html">
    <link rel="import" href="bower_components/paper-spinner/paper-spinner.html">
    <link rel="import" href="bower_components/paper-styles/color.html">
    <link rel="import" href="bower_components/paper-styles/typography.html">
    <link rel="import" href="bower_components/iron-form/iron-form.html">
    <link rel="import" href="bower_components/paper-styles/demo-pages.html">
    <link rel="import" href="bower_components/paper-button/paper-button.html">
    <link rel="import" href="bower_components/paper-drawer-panel/paper-drawer-panel.html">
    <link rel="import" href="bower_components/paper-styles/paper-styles.html">
    <link rel="import" href="bower_components/paper-styles/demo-pages.html">
    <link rel="import" href="bower_components/paper-header-panel/paper-header-panel.html">

    <style>
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
    </style>

 </head>

 <body>
    <paper-drawer-panel>

        <paper-header-panel drawer class="cyan x-scope paper-header-panel-0" style="width:256px;">

            <paper-toolbar>
                <div class="paper-header animate">Dashboard</div>
            </paper-toolbar>

            <paper-menu>
                <a href="index.php?page=Home"><paper-item>Home</paper-item></a>
                <a href="index.php?page=New%20Vehicle%20Registration"><paper-item>New Vehicle Registration</paper-item></a>
                <a href="index.php?page=Auto%20Transaction"><paper-item>Auto Transaction</paper-item></a>
                <a href="index.php?page=Driver%20License%20Registration"><paper-item>Driver License Registration</paper-item></a>
                <a href="index.php?page=Violation%20Record"><paper-item>Violation Record</paper-item></a>
                <a href="#"><paper-item>Searches</paper-item></a>
            </paper-menu>

            </paper-header-panel>

            <paper-header-panel main class="blue x-scope paper-header-panel-0" style="width:100%">

            <paper-toolbar>
                <div class="paper-header animate">
			<?php 
				$header= 'Home';
				if (!empty($_GET['page'])) {
					$header = $_GET['page'];
				}
				echo $header;
			?>
		</div>
            </paper-toolbar>

            <div id="contents" style="padding-left:20px; padding-right:20px">
		<?php
			$contents = file_get_contents('Home.html');
			if (!empty($_GET['page'])) {
				$contents = file_get_contents($_GET['page'] . '.html');
			}
			echo $contents;
		?>
            </div>

        </paper-header-panel>

    </paper-drawer-panel>

</body>
</html>
