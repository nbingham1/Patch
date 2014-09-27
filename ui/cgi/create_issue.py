#!/usr/bin/python
 
import cgi
import MySQLdb as db


form = cgi.FieldStorage()
 
issue = form.getvalue('issue')


con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()
try:
	cur.execute("insert into issues (issue) values (%s)", (issue));
	con.commit()
except:
	con.rollback()

result = cur.fetchall()

if con:
	con.close()
 
# headers 
print "Content-type: text/html"
print 

# data
