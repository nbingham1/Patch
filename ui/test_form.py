#!/usr/bin/env python
 
import cgi
 
form = cgi.FieldStorage()
 
val1 = form.getvalue('comments')
 
print "Content-type: text/html"
print 
print "The form input is below...<br/>"
print val1
