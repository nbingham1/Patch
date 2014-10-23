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
f1 = open('./data/article1.txt')
a = f1.read()
a = a.decode('utf-8').encode('ascii','ignore')
#a = "Edward dog tree" 
text1 = TextBlob(a)

f2 = open('./data/articleFox.txt')
b = f2.read()
#b = "Mary dog"
text2 = TextBlob(b)


#wl1_nn = extract_words(text1, "NN")
#wl1_nnp = extract_words(text1, "NNP")
#diff(wl1_nn,wl1_nnp)

print "list_path_similarity of the two articles: "
print blob_path_similarity(text1, text2, 10, "NN")

print "proper noun similarity of the two articles: "
print blob_rhine_similarity(text1, text2, 4, "NNP")


#sentence_dist = path_similarity_flow(text1.sentences, 5, "NN")
print "Starting rhine"
rhine_dist = rhine_n_similarity_flow(text1.sentences, 2, "NNP", 1)
#rhine_dist1 = rhine_n_similarity_flow(text1.sentences, 2, "NNP", 1)
print "Left rhine "

sents = []

for n in [1,2,3]:
    sents.append(path_n_similarity_flow(text1.sentences, 5, "NN",n))

sents.append(rhine_dist)
#sents.append(rhine_dist1)

flow = flow_fusion(sents, 4)


args = find_arguments(flow)
plotter ([flow, sents[0], rhine_dist], args, 666)

'''
figure()
plot(sents[0], 'o-')
xlabel("Sentence number")
ylabel("correlation")

figure()
plot(rhine_dist, 'o-')
xlabel("Sentence number")
ylabel("correlation")


figure()
plot(flow, 'o-')
xlabel("Sentence number")
ylabel("correlation")


for i in xrange(len(text1.sentences)):
    print i
    print text1.sentences[i]


args = find_arguments(flow)

for el in args:
    axvline(x=el, ymin=0, linewidth=1, color='r')
show()

'''


