#!/usr/bin/python
 
import cgi
import MySQLdb as db
import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()

cur.execute("select issue from issues");

results = cur.fetchall()

if con:
	con.close()
 
# headers 
print "Content-type: text/html"
print 

# data
for result in results:
	print '<div class="issue">'
	sentences = TextBlob(result[0]).sentences
	
	print '</div>'
