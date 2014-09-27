from textblob import Word
from textblob.wordnet import VERB
word = Word("octopus")
print word.synsets
print Word("hack").get_synsets(pos=VERB)
