#!/usr/bin/python
 
import cgi
import MySQLdb as db

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()
cur.execute("select issue from issues where id=1");
result = cur.fetchall()

if con:
	con.close()

 
form = cgi.FieldStorage()
 
issue = form.getvalue('issue')

# headers 
print "Content-type: text/html"
print 

# data
print issue
print result
