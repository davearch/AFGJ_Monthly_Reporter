============================
 AFGJ Monthly Reporter
============================

Description
===========

In-house program to move our downloaded monthly reports to our Dropbox Folder

Features
--------

* Prompts you to select the folder with your downloaded excel sheets
* Matches the reports with their respective Dropbox directories
* Moves each report to the correct folder and automatically renames them based on the date

Authors
=======

David A Archuleta, Jr. 2020

Requirements
============

* Python 3
* Tkinter

Usage
=====

To start the application, run::

  python3 AFGJ_Monthly_Reporter/monthly_reporter.py


General Notes
=============

This program is based on our workflow of having excel sheets emailed to us monthly.


TODOS
=============
* improve this program to automatically download the correct files from QuickBooks.
* implement logging system instead of printing things to stdout
* fix excel memory leaks
* implement more excel work to highlight final balance
* implement more excel work to append latest month to single workbook, if applicable
* fix monthly report folder mistakes, sometimes the program doesn't correctly identify the correct folder
* build program to exe file with pyinstaller
* optimize (too slow now after the excel stuff)