#!/usr/bin/python
 
import cgi
import MySQLdb as db
import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn
from api import *
from api2 import *

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
	print representative_blob(TextBlob(result[0]), 3, "NN")
	print '</div>'
