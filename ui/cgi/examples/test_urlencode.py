#!/usr/bin/python
 
import cgi
 
form = cgi.FieldStorage()
 
val1 = form.getvalue('first')
val2 = form.getvalue('last')
 
print "Content-type: text/html"
print 
print "<html><head><title>Test URL Encoding</title></head><body>"
print "Hello my name is %s %s </body></html>" % (val1, val2)
