#!/usr/bin/python
 
import cgi
import MySQLdb as db
import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn
from api import *
from api2 import *


form = cgi.FieldStorage()
 
issue = form.getvalue('issue')
sentences = TextBlob(issue).sentences
rep = representative_blob(sentences, 5, "NN")

con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
cur = con.cursor()
try:
	cur.execute("insert into issues (rep) values (%s)", (rep));
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
