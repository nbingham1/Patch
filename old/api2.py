import nltk
import textblob as tb
from nltk.corpus import wordnet as wn

def freqGet(howMany, wordList):
    fdist = nltk.FreqDist(wordList)
    top = []
    for el in fdist.most_common(howMany):
        top.append(el[0])
    return top

def freqGetTuple(howMany, wordList):
    fdist = nltk.FreqDist(wordList)
    return fdist.most_common(howMany)

#Takes in a text string
def getWordSubjectivity(text):
    textblob = tb.TextBlob(text)
    return textblob.sentiment.subjectivity

#Takes in a text string
def getSentenceSubjectivity(text):
    textblob = tb.TextBlob(text)
    accum = 0
    for sentence in textblob.sentences:
        accum += sentence.sentiment.subjectivity
    return accum/len(textblob.sentences)

#Takes in a text string
def getWordPolarity(text):
    textblob = tb.TextBlob(text)
    return textblob.sentiment.polarity

#Takes in a text string
def getSentencePolarity(text):
    textblob = tb.TextBlob(text)
    accum = 0
    for sentence in textblob.sentences:
        accum += sentence.sentiment.polarity
    return accum/len(textblob.sentences)

def percentPositiveSentences(text):
    THRESH = .04
    textblob = tb.TextBlob(text)
    accum = 0
    for sentence in textblob.sentences:
        if sentence.sentiment.polarity > THRESH:
            accum += 1
    return accum#/len(textblob.sentences)

def percentNegativeSentences(text):
    THRESH = -.04
    textblob = tb.TextBlob(text)
    accum = 0
    for sentence in textblob.sentences:
        if sentence.sentiment.polarity < THRESH:
            accum += 1
    return accum#/len(textblob.sentences)

