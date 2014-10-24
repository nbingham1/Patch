#!/usr/bin/python
 
import cgi
import beanstalkc

# headers 
print "Content-type: text/html"
print 

# data
form = cgi.FieldStorage()

issue = form.getvalue('issue')
issue = issue.decode('utf-8').encode('ascii', 'ignore')

beanstalk = beanstalkc.Connection(host='localhost', port=11300)
beanstalk.put(issue)
beanstalk.close()
