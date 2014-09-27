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
#a = "Edward dog tree" 
text1 = TextBlob(a)

f2 = open('./data/article2.txt')
b = f2.read()
#b = "Mary dog"
text2 = TextBlob(b)



######

wl1_nn = extract_words(text1, "NN")
wl1_nnp = extract_words(text1, "NNP")
diff(wl1_nn,wl1_nnp)

freq1_nn = freqGetTuple(50, wl1_nn)
print freq1_nn
synsets1 = tuples_to_synsets(freq1_nn, "NN")

freq1_nnp = freqGetTuple(5, wl1_nnp)
print freq1_nnp
synsets1_nnp = tuples_to_synsets(freq1_nnp, "NNP")
#######

wl2_nn = extract_words(text2, "NN")
wl2_nnp = extract_words(text2, "NNP")
diff(wl2_nn,wl2_nnp)

freq2_nn = freqGetTuple(50, wl2_nn)
print freq2_nn
synsets2 = tuples_to_synsets(freq2_nn, "NN")

freq2_nnp = freqGetTuple(5, wl2_nnp)
print freq2_nnp
synsets2_nnp = tuples_to_synsets(freq2_nnp, "NNP")

######
print "list_path_similarity of the two articles: "
print list_path_similarity(synsets1, synsets2)

print "pronoun similarity of the two articles: "
print list_path_similarity(synsets1_nnp, synsets2_nnp)
print rhine_similarity(freq1_nnp, freq2_nnp)

#print extract_words(wiki, "NN").path_similarity(extract_words(wiki2, "NN"))


# This list will be a list of distances, indexed by sentence, of a word block
'''
sentence_dist = path_similarity_flow(text1, 5, "NN")
sentence_dist1 = path_n_similarity_flow(text1, 5, "NN",1)
sentence_dist2 = path_n_similarity_flow(text1, 5, "NN",2)
sentence_dist3 = path_n_similarity_flow(text1, 5, "NN",3)
sentence_dist4 = path_n_similarity_flow(text1, 5, "NN",4)
#sentence_dist2 = path_similarity_flow(text1, 5, "VB")

sentence_combine = []

for i in xrange(len(sentence_dist)):
    sentence_combine.append(sentence_dist1[i] + .7*sentence_dist2[i] + .5*sentence_dist3[i])

for i in xrange(len(sentence_combine)-2):
    sentence_combine[i] = .4*sentence_combine[i] + .4*sentence_combine[i+1] + .2*sentence_combine[i+2]

figure()
plot(sentence_dist1, 'o-')
xlabel("Sentence number")
ylabel("correlation")

figure()
plot(sentence_dist2, 'o-')

figure()
plot(sentence_dist3, 'o-')

figure()
plot(sentence_combine, 'o-')


#for i in xrange(len(text1.sentences)):
#    print i
#    print text1.sentences[i]


show()
'''
