import nltk
import math
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn
from api2 import *
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

def rhine_similarity(words1, words2):
	pairs = []
	for word1 in words1:
		for word2 in words2:
                        dist = rb.freshRhine().distance(word1[0],word2[0])
                        if math.isnan(dist):
                            dist = 0
                        else:
                            dist = 30/(dist+29)
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

def blob_rhine_similarity(blob1, blob2, count, pos):
	wl1 = extract_words(blob1, pos)
	wl2 = extract_words(blob2, pos)
	fr1 = freqGetTuple(count, wl1)
	fr2 = freqGetTuple(count, wl2)
	return rhine_similarity(fr1, fr2)


def path_similarity_flow(blob, count, pos):
	sentences = blob.sentences
	y = []
        y.append(0)
        for i in xrange(1,len(sentences)):
		y.append(blob_path_similarity(sentences[i], sentences[i-1], count, pos))
	return y

def path_n_similarity_flow(blob, count, pos, n):
	sentences = blob.sentences
	y = []
        for i in xrange(n):
            y.append(0)
        for i in xrange(n,len(sentences)):
	    y.append(blob_path_similarity(sentences[i], sentences[i-n], count, pos))
	return y

def rhine_n_similarity_flow(blob, count, pos, n):
	sentences = blob.sentences
	y = []
        for i in xrange(n):
            y.append(0)
        for i in xrange(n,len(sentences)):
	    y.append(blob_rhine_similarity(sentences[i], sentences[i-n], count, pos))
	return y

def representative_blob(blobs, count, pos):
	scores = [0] * len(blobs)
        for i in xrange(len(blobs)):
                for j in xrange(i+1, len(blobs)):
                        sim = blob_path_similarity(blobs[i], blobs[j], count, pos)
                        scores[i] += sim
			scores[j] += sim
        
	return blobs[scores.index(max(scores))]
