import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet as wn

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
		synsets.append([wn.synset(word[0] + "." + wordnet_pos(pos) + ".01"), word[1]])
	return synsets



wiki = TextBlob("The dog ran around the flag pole.")
wiki2 = TextBlob("Dogs like poles, but not flags.")

print extract_words(wiki, "NN")


#print extract_words(wiki, "NN").path_similarity(extract_words(wiki2, "NN"))

