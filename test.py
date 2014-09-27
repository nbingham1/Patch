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

rhine_dist = rhine_n_similarity_flow(sentences, 5, "NNP", 1)

sents = []

for n in [1,2,3,4]:
    sents.append(path_n_similarity_flow(sentences, 5, "NN", n))

sents.append(rhine_dist)

flow = flow_fusion(sents, 5)

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
print representative_blob(arg_reps, 10, "")

