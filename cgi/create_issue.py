#!/usr/bin/python
 
import cgi
import beanstalkc
import requests
from bs4 import BeautifulSoup

# headers 
print "Content-type: text/html"
print 

# data
form = cgi.FieldStorage()

issue = ""
if 'issue' in form:
	issue = form['issue']
elif 'url' in form:
	url = form['url']
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	for p in soup.body.findAll("p"):
	        issue += p.text

issue = issue.decode('utf-8').encode('ascii', 'ignore')

if issue != "":
	beanstalk = beanstalkc.Connection(host='localhost', port=11300)
	beanstalk.put(issue)
	beanstalk.close()
