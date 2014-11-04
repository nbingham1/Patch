#!/usr/bin/python
import cgi, cgitb
import MySQLdb as db

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()

form = cgi.FieldStorage()

keys = []
#check the form
if 'expand' in form and 'level' in form:
	keys.append(form.getvalue('expand'))
	keys.append(form.getvalue('level'))

# update cookie
print("Content-type: text/html\r\n\r\n")

query = "select s0.id,s1.level,s0.data from statements s0 inner join statementlinks s1 on s0.id=s1.child where s1.parent=%s and s1.level=%s"

cur.execute(query, keys)
results = cur.fetchall()

if keys[1] == '0':
	print '<p>'
for result in results:
	if result[1] > 0:
        	print('   <p id="statement-' + str(result[0]) + '">')
                print('<a class=sentence onclick="update(' + str(result[0]) + ', ' + str(result[1]-1) + ')">')
                print('<b>')
        print result[2]
        if result[1] > 0:
                print('</b>')
                print('</a>')
        	print('</p>')
if keys[1] == '0':
	print '</p>'

if con:
	con.close()
