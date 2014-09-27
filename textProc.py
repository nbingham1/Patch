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

'''
f1 = open('./data/article1.txt')
f2 = open('./data/articleFox.txt')
a = f1.read()
b = f2.read()

print "article1:"
print "Word Subjectivity: "
print getWordSubjectivity(a)
print "Sentence Subjectivity: "
print getSentenceSubjectivity(a)

print "Fox article:"
print "Word Subjectivity: "
print getWordSubjectivity(b)
print "Sentence Subjectivity: "
print getSentenceSubjectivity(b)


print "article1:"
print "Word Polarity: "
print getWordPolarity(a)
print "Sentence Polarity: "
print getSentencePolarity(a)

print "Fox article:"
print "Word Polarity: "
print getWordPolarity(b)
print "Sentence Polarity: "
print getSentencePolarity(b)

print "article1 percent positive sentences:"
print percentPositiveSentences(a)
print "article1 percent negative sentences:"
print percentNegativeSentences(a)


print "Fox article percent positive sentences:"
print percentPositiveSentences(b)
print "Fox article percent negative sentences:"
print percentNegativeSentences(b)




#text1 = tb.TextBlob(a)
#text2 = tb.TextBlob(b)


'''

'''
wiki = tb.TextBlob("The canine jogged accross the Walmart parking location.")
wiki1 = tb.TextBlob("The election year politics are annoying for many people.")
wiki2 = tb.TextBlob("The dog was a pretty dog.")

#print wiki.tags

for i in xrange(len(wiki.words)):
    print wiki.words[i].lemmatize()

print wiki
print wiki.sentiment.subjectivity
print wiki2.sentiment.subjectivity
'''
'''
f1 = open('./data/article1.txt')
f2 = open('./data/articleFox.txt')
a = f1.read()
b = f2.read()
#a = a.replace('\n', ' ').replace('\r', '')
#b = b.replace('\n', ' ').replace('\r', '')

text1 = tb.TextBlob(a)
text2 = tb.TextBlob(b)
'''
'''
print "The normal article polarity/subjectivity"
print text1.sentiment.polarity
print text1.sentiment.subjectivity

print "The fox article polarity/subjectivity"
print text2.sentiment.polarity
print text2.sentiment.subjectivity
'''
'''
myText = nltk.Text(a)


print text1.words

fdist1 = nltk.FreqDist(text1.words)

print fdist1.most_common(7)

top7 = []
for el in fdist1.most_common(7):
    top7.append(el[0])

print top7
myText.dispersion_plot(top7)
'''


