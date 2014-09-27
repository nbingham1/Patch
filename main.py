import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn
from textProc import *

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
		if pos in tag[1]:
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
		synsets.append([word[0].get_synsets(pos=wordnet_pos(pos))[0], word[1]])
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
		score += pair[0]*pair[1]
		total += pair[1]
	
	score /= total	

	return score

wiki = TextBlob("The dog ran around the flag pole.")
wiki2 = TextBlob("Dogs like poles, but not flags.")

wordlist1 = extract_words(wiki, "NN")
freq1 = freqGetTuple(10, wordlist1)
synsets1 = tuples_to_synsets(freq1, "NN")

wordlist2 = extract_words(wiki2, "NN")
freq2 = freqGetTuple(10, wordlist2)
synsets2 = tuples_to_synsets(freq2, "NN")

print list_path_similarity(synsets1, synsets2)

#print extract_words(wiki, "NN").path_similarity(extract_words(wiki2, "NN"))

