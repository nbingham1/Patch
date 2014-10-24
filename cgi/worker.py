#!/usr/bin/python
import cgi
import MySQLdb as db
import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn
from api import *
from api2 import *
import beanstalkc

beanstalk = beanstalkc.Connection(host='localhost', port=11300)
while 1:
        job = beanstalk.reserve()

	issue = str(job.body)
	
	sentences = TextBlob(issue).sentences
	
	rhine_dist = rhine_n_similarity_flow(sentences, 5, "NNP", 1)
	sents = []
	for n in [1,2,3]:
	    sents.append(path_n_similarity_flow(sentences, 10, "NN", n))

	sents.append(rhine_dist)
	flow = flow_fusion(sents, 4)
	minima = find_arguments(flow)
	
	args = []
	for i in xrange(len(minima)):
	        if i+1 < len(minima):
	                args.append(sentences[minima[i]:minima[i+1]-1])
	        else:
	                args.append(sentences[minima[i]:])

	arg_reps = []
	for arg in args:
	        arg_reps.append(representative_blob(arg, 10, "NN"))

	rep = representative_blob(arg_reps, 10, "NN")
	
	con = db.connect('localhost', 'patch', 'democracy in action', 'patch')
	cur = con.cursor()
	try:
	        cur.execute("insert into issues (rep) values (%s)", (rep,))
	        con.commit()
	        issue_id = cur.lastrowid

	        for i in xrange(len(args)):
	                cur.execute("insert into arguments (rep,issue) values (%s,%s)", (arg_reps[i], issue_id))
	                con.commit()
	                argument_id = cur.lastrowid
	                for sent in args[i]:
	                        cur.execute("insert into sentences (argument,sentence) values (%s,%s)", (argument_id,sent))
	                        con.commit()
	
	except:
	        con.rollback()
	
	result = cur.fetchall()
	
	if con:
	        con.close()

	plotter([flow, sents[0], rhine_dist], minima, issue_id)

	job.delete()
beanstalk.close()
