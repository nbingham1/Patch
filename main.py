import nltk
from textblob import Word
from textblob.wordnet import VERB
from textblob import TextBlob


def extract_nouns(blob):
	nouns = []
	tags = blob.tags
	for tag in tags:
		if "NN" in tag[1]:
			nouns.append(tag[0])
	return nouns

wiki = TextBlob("The dog ran around the flag pole.")
wiki2 = TextBlob("Dogs like poles, but not flags.")

print extract_nouns(wiki)

