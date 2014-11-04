#!/usr/bin/python
import cgi, cgitb
import Cookie
import os
import MySQLdb as db
import beanstalkc
import pickle

form = cgi.FieldStorage()
cookie = Cookie.SimpleCookie()

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()

uname = ""
uid = -1
if 'logout' in form:
	cookie['uname'] = ""
	cookie['uid'] = ""
	print(cookie)
elif 'uname' in form:
	uname = form['uname'].value
	cur.execute("select id from users where name=%s", (uname,))
	results = cur.fetchall()
	if results:
		uid = results[0][0]
		cookie['uname'] = uname
		cookie['uid'] = uid
		print(cookie)
	else:
		cur.execute("insert into users (name) value (%s)", (uname,))
		con.commit()
		results = cur.fetchall()
		cur.execute("select id from users where name=%s", (uname,))
        	results = cur.fetchall()
		uid = results[0][0]
                cookie['uname'] = uname
                cookie['uid'] = uid
                print(cookie)
else:
	cookie_string = os.environ.get('HTTP_COOKIE')
	if cookie_string:
		cookie.load(cookie_string)
		uname = cookie['uname'].value
		uid = cookie['uid'].value

if 'issue' in form and uid:
	issue = form['issue'].value.decode('utf-8').encode('ascii', 'ignore')

	if issue != "":
	        beanstalk = beanstalkc.Connection(host='localhost', port=11300)
	        beanstalk.put(pickle.dumps({'uid':uid, 'issue':issue}))
	        beanstalk.close()

results = []
if uname != "":
	cur.execute("select s.id,u.level,s.data from statements as s inner join userlinks as u on s.id=u.sid where u.uid=%s", (uid,))
	results = cur.fetchall()

# headers
print("Content-type: text/html\r\n\r\n")
print('<html>')
print(' <head>')
print('  <title>Patch</title>')
print('  <link rel="stylesheet" type="text/css" href="/index.css">')
print('  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>')
print('  <script type="text/javascript" src="/js/api.js"></script>')
print(' </head>')
print(' <body>')
print('  <div id="menu-bar">')
print('   <div id="profile-marker">')
if uname == "":
	print('    <form>')
	print('     <input id="profile-uname" type="text" name="uname">')
	print('     <input id="profile-login" type="submit" value="Login">')
	print('    </form>')
else:	
	print('    <form id="profile-name">')
	print(uname)
	print('    <input type="hidden" name="logout" value=1>')
        print('    <input id="profile-logout" type="submit" value="Logout">')
        print('    </form>')
print('   </div>')
print('  </div>')
print('  <div id="profile-issues">')
if uname != "":
	print('    <form id="create-issue" method="post">')
	print('     <textarea id="write-issue" name="issue"></textarea>')
	print('     <input id="submit-issue" type="submit" value="Create">')
	print('    </form>')
for result in results:
	print('   <div class="profile-issue">')
	print('   <p id="statement-' + str(result[0]) + '">')
        if result[1] > 0:
		print('<a class=sentence onclick="update(' + str(result[0]) + ', ' + str(result[1]-1) + ')">')
        	print('<b>')
        print result[2]
	if result[1] > 0:
        	print('</b>')
		print('</a>')
        print('</p>')	
	print('   </div>')
print('  </div>')
print(' ')
print(' </body>')
print('</html>')

if cur:
	cur.close()

if con:
	con.close()
