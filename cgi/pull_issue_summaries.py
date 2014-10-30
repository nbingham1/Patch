#!/usr/bin/python
 
import cgi
import MySQLdb as db

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()

cur.execute("select * from issues");

results = cur.fetchall()

if con:
	con.close()
 
# headers 
print("Content-type: text/html")
print("")

# data
for result in results:
	print('<div class="item" id="item_' + str(result[0]) + '" onclick="$(\'#account_pane\').hide(); $(\'#issue_pane\').show(); pull_argument_summaries(\'' + str(result[0]) + '\', function(data, response){ $(\'#issue_pane_content\').html(data); });">')
	print(result[1])
	print('</div>')
