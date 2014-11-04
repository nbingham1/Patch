#!/usr/bin/python
 
import cgi
import MySQLdb as db

form = cgi.FieldStorage()

issue = form.getvalue('issue')

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()

cur.execute("select id,rep from arguments where issue=%s", (issue,));

results = cur.fetchall()

if con:
	con.close()
 
# headers 
print "Content-type: text/html"
print 

# data
for result in results:
	print '<div class="item" id="item_' + str(result[0]) + '" onclick="$(\'#issue_pane\').hide(); $(\'#argument_pane\').show(); pull_sentences(\'' + str(result[0]) + '\', function(data, response){ $(\'#argument_pane_content\').html(data); }); ">'
	print result[1]
	print '</div>'
