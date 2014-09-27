#!/usr/bin/python
 
import cgi
import MySQLdb as db

form = cgi.FieldStorage()

argument = form.getvalue('argument')

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()

cur.execute("select sentence from sentences where argument=%s", (argument));

results = cur.fetchall()

if con:
	con.close()
 
# headers 
print "Content-type: text/html"
print 

# data
for result in results:
	print '<div class="item">'
	print result[0]
	print '</div>'
