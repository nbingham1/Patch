#!/usr/bin/python
import cgi
import MySQLdb as db
import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet
from lang import *
import beanstalkc
import pickle

beanstalk = beanstalkc.Connection(host='localhost', port=11300)
while 1:
        job = beanstalk.reserve()
	work = pickle.loads(str(job.body))
	issue = work['issue']
	uid = work['uid']
	
	if uid and issue:
		print "Starting Processing for " + str(uid)
	
		sentences = TextBlob(issue).sentences
		parent_indices = create_tree(sentences, "NN", "", [[1, 0.5], [2, 0.25], [3, 0.125], [4, 0.125]])
		print("Linguistic Processing Done")	
		indices = []

		print parent_indices
	
		con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
		cur = con.cursor()
		try:
		        for i in xrange(len(sentences)):
		                cur.execute("insert into statements (data) values (%s)", (str(sentences[i]),))
		                con.commit()
		                indices.append(cur.lastrowid)
	
			level = 0
			found = True
			while found:
				found = False
				for i in xrange(len(parent_indices)):
					if parent_indices[i][1] == level and indices[i] == indices[parent_indices[i][0]]:
						cur.execute("insert into userlinks (uid, sid, level) values (%s, %s, %s)", (str(uid), str(indices[i]), str(level)))
                                                con.commit()
						found = True
					elif parent_indices[i][1] == level and indices[i] != indices[parent_indices[i][0]]:
                                                cur.execute("insert into statementlinks (parent, child, level) values (%s, %s, %s)", (str(indices[parent_indices[i][0]]), str(indices[i]), str(level)))
						con.commit()
						found = True
					elif parent_indices[i][1] > level:
						cur.execute("insert into statementlinks (parent, child, level) values (%s, %s, %s)", (str(indices[i]), str(indices[i]), str(level)))
						con.commit()
						found = True
				level += 1

			print ("Done")	
		except e:
			print e
			print("Exception")
		        con.rollback()
		
		if con:
		        con.close()
	else:
		print "Error: Invalid work"

	job.delete()
beanstalk.close()
