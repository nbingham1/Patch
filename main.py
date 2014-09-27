import nltk
import math
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn
from textProc import *
import matplotlib as plt 
from pylab import *
from rhine import *
from rhine_reader import *


rb = RhineBundle()
rb.rhineGenerate('Rhine.txt')
#To get a fresh rhine request, do rb.freshRhine() which returns a rhine

def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]

def wordnet_pos(treebank_pos):
	if "NN" in treebank_pos:
		return wn.NOUN
	elif "JJ" in treebank_pos:
		return wn.ADJ
	elif "RB" in treebank_pos:
		return wn.ADV
	elif "VB" in treebank_pos:
		return wn.VERB
	else:
		return ''

def extract_words(blob, pos):
	words = []
	tags = blob.tags
	for tag in tags:
		if pos == "" or pos in tag[1]:
			words.append(tag[0])
	return words

def words_to_synsets(words, pos):
	synsets = []
	for word in words:
		synsets.append(wn.synset(word[0] + "." + wordnet_pos(pos) + ".01"))
	return synsets


def tuples_to_synsets(words, pos):
        synsets = []
	for word in words:
		synset = []
		if pos == "":
			synset = Word(word[0]).get_synsets()
		else:
                	synset = Word(word[0]).get_synsets(pos=wordnet_pos(pos))
                if len(synset) > 0:
		    synsets.append([synset[0], word[1]])
	return synsets

def list_path_similarity(words1, words2):
	pairs = []
	for word1 in words1:
		for word2 in words2:
			pairs.append([word1[0].path_similarity(word2[0]), min(word1[1], word2[1]), word1[0], word2[0]])
	pairs.sort(reverse=True)
	covered1 = []
	covered2 = []
	remove = []
	for index, pair in enumerate(pairs):
		if pair[2] in covered1 and pair[3] in covered2:
			remove.append(index)
		else:
			if pair[2] not in covered1:
				covered1.append(pair[2])
			if pair[3] not in covered2:
				covered2.append(pair[3])

        print pairs

	remove.sort(reverse=True)
	for idx in remove:
		pairs.pop(idx)
        print pairs

	total=0
	score=0
	for pair in pairs:
		if pair[0] is not None and pair[1] is not None:
			score += pair[0]*pair[1]
			total += pair[1]

	if total != 0:	
		score /= total	

	return score

def rhine_similarity(words1, words2):
	pairs = []
	for word1 in words1:
		for word2 in words2:
                        print word1[0]
                        print word2[0]
                        dist = rb.freshRhine().distance(word1[0],word2[0])
                        if math.isnan(dist):
                            dist = 100
                        dist = dist/100
			pairs.append([dist, min(word1[1], word2[1]), word1[0], word2[0]])
	pairs.sort(reverse=True)
	covered1 = []
	covered2 = []
	remove = []
	for index, pair in enumerate(pairs):
		if pair[2] in covered1 and pair[3] in covered2:
			remove.append(index)
		else:
			if pair[2] not in covered1:
				covered1.append(pair[2])
			if pair[3] not in covered2:
				covered2.append(pair[3])

	remove.sort(reverse=True)
	for idx in remove:
		pairs.pop(idx)

	total=0
	score=0
	for pair in pairs:
		if pair[0] is not None and pair[1] is not None:
			score += pair[0]*pair[1]
			total += pair[1]

	if total != 0:
		score /= total	

	return score

def blob_path_similarity(blob1, blob2, count, pos):
	wl1 = extract_words(blob1, pos)
	wl2 = extract_words(blob2, pos)
	fr1 = freqGetTuple(count, wl1)
	fr2 = freqGetTuple(count, wl2)
	sn1 = tuples_to_synsets(fr1, pos)
	sn2 = tuples_to_synsets(fr2, pos)
	return list_path_similarity(sn1, sn2)

def path_similarity_flow(blob, count, pos):
	sentences = blob.sentences
	y = []
        for i in xrange(len(sentences)-1):
		y.append(blob_path_similarity(sentences[i], sentences[i+1], count, pos))
	return y




# Pull out news articles
f1 = open('./data/article1.txt')
a = f1.read()
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
#print rhine_similarity(freq1_nnp, freq2_nnp)

#print extract_words(wiki, "NN").path_similarity(extract_words(wiki2, "NN"))


# This list will be a list of distances, indexed by sentence, of a word block

sentence_dist = path_similarity_flow(text1, 5, "NN")
sentence_dist2 = path_similarity_flow(text1, 5, "VB")

sentence_dist3 = []

for i in xrange(len(sentence_dist)):
	sentence_dist3.append(sentence_dist[i] + sentence_dist2[i])


plot(sentence_dist3,'o-')
xlabel("Sentence number")
ylabel("correlation")
for i in xrange(len(text1.sentences)):
    print i
    print text1.sentences[i]

show()
