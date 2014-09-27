import nltk
import math
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn
import matplotlib as plt 
from pylab import *

import sys

sys.path.append("ui/cgi")

from api import *
from api2 import *
from rhine import *
from rhine_reader import *


# Pull out news articles
f1 = open('./data/articleFox.txt')
a = f1.read()
a = a.decode('utf-8').encode('ascii','ignore')
text1 = TextBlob(a)
sentences = text1.sentences
'''
rhine_dist = rhine_n_similarity_flow(sentences, 3, "NNP", 1)

sents = []

for n in [1,2,3]:
    sents.append(path_n_similarity_flow(sentences, 5, "NN", n))

sents.append(rhine_dist)

flow = flow_fusion(sents, 4)

minima = find_arguments(flow)

args = []

for i in xrange(len(minima)):
	if i+1 < len(minima):
        	args.append(sentences[minima[i]:minima[i+1]-1])
	else:
		args.append(sentences[minima[i]:])

print "Arguments:"
for arg in args:
	print arg
	print
	print

arg_reps = []

for arg in args:
	arg_reps.append(representative_blob(arg, 10, ""))

print "Argument Representative Blobs:"
for rep in arg_reps:
	print rep
	print

print "Article Representative Blob:"
rblob = representative_blob(arg_reps, 10, "")
'''

a = TextBlob('Goldman Sachs has long had a comprehensive approach for addressing potential conflicts, the New York based bank said in a statement.')
b = TextBlob('Mr Shelby stated that no one in the financial industry should be able to buy their way out from culpability when it is so strong it defies rationality - I agree with Warren on that.')
c = TextBlob('It is unacceptable if, because of lack of preparedness and planning and global preperation, people are dying.')
d = TextBlob('So, it should be no suprise then that, last week, Secretary of State John Kerry, told the United Nation\'s Security Council that in the fight against the Islamic State, There is a role for nearly every country in the world to play, including Iran')
e = TextBlob('The kitty liked to play with the pretty bear')

rblobs = [a,b,c,d,e]

clusters = []
for i in xrange(len(rblobs)):
    idx = is_in_cluster(rblobs[i],clusters)
    if idx == -1:
        clusters.append(rblobs[i])
        print "Forming new cluster: "
        print rblobs[i]
    else:
        print rblobs[i]
        print 
        print
        print " paired with "
        print
        print
        print clusters[idx]




