import nltk
from textblob import *
from textblob.wordnet import *
from nltk.corpus import wordnet
from rhine import *
from rhine_reader import *
import math
import matplotlib
from pylab import *
import pydot


rb = RhineBundle()
rb.rhineGenerate('/var/www/patch/Rhine.txt')

def wordnet_pos(treebank_pos):
	if "NN" in treebank_pos:
		return wordnet.NOUN
	elif "JJ" in treebank_pos:
		return wordnet.ADJ
	elif "RB" in treebank_pos:
		return wordnet.ADV
	elif "VB" in treebank_pos:
		return wordnet.VERB
	else:
		return ''

def word_list(blob, pos):
	results = []
        tags = TextBlob(blob).tags
        for tag in tags:
                if not pos or pos in tag[1]:
			found = False
			for result in results:
				if result[0] == tag[0] and result[1] == tag[1]:
					result[2]+=1
					found = True
			if not found:
                        	results.append([tag[0], tag[1], 1])

        return results

word_similarity_cache = {}

def word_similarity(word0, word1):
	key = ()
	if word0[0] < word1[0]:
		key = (word0[0], word0[1], word1[0], word1[1])
	else:
		key = (word1[0], word1[1], word0[0], word0[1])

	if key in word_similarity_cache:
		result = word_similarity_cache[key]
		return result

	result = 0
	if "NNP" in word0[1] and "NNP" in word1[1]:
		try:
			dist = rb.freshRhine().distance(word0[0], word1[0])
                	if not math.isnan(dist):
                		result = 30/(dist+29)
		except:
			rb.timeouts+=1
		result=0
	else: 
		try:
			syn0 = wordnet.synset(word0[0] + "." + wordnet_pos(word0[1]) + ".01")
			syn1 = wordnet.synset(word1[0] + "." + wordnet_pos(word1[1]) + ".01")
	
			result = syn0.path_similarity(syn1)
		except:
			result = 0
	
	word_similarity_cache[key] = result
	return result

def blob_similarity(blob0, blob1, pos):
	words0 = word_list(blob0, pos)
	words1 = word_list(blob1, pos)

	matching = []
        for word0 in words0:
		if "NNP" not in word0[1]:
         	       for word1 in words1:
                	        matching.append([word_similarity(word0, word1), min(word0[2], word1[2]), word0[0], word1[0]])
        matching.sort(reverse=True)

        covered_words0 = []
        covered_words1 = []
        remove = []
        for index, match in enumerate(matching):
                if match[2] in covered_words0 or match[3] in covered_words1:
                        remove.append(index)
                else:
                        if match[2] not in covered_words0:
                                covered_words0.append(match[2])
                        if match[3] not in covered_words1:
                                covered_words1.append(match[3])

        remove.sort(reverse=True)
        for idx in remove:
                matching.pop(idx)

        total = 0
        score = 0
        for match in matching:
                if match[0] is not None and match[1] is not None:
                        score += match[0]*match[1]
                        total += match[1]

        if total != 0:
                score /= total

        return score

def blob_flow(blobs, pos, coeffs):
        y = [0 for x in xrange(len(blobs))]
        for x in xrange(len(blobs)):
		for coeff in coeffs:
			if x >= coeff[0]:
            			y[x] += coeff[1]*blob_similarity(str(blobs[x]), str(blobs[x-coeff[0]]), pos)

        return y

def convolute(y, coeffs):
    for i in xrange(len(y)-len(coeffs)):
        preval = y[i]
        for j in xrange(len(coeffs)):
            y[i] += y[i+j]*coeffs[j]
        y[i] -= preval
    return y

def minima(y, n):
	m = []
	m.append([y[0], 0])
	for x in xrange(1, len(y)-1):
		if (y[x-1] > y[x]) and (y[x+1] > y[x]):
			m.append([y[x], x])
	m.append([0, len(y)])
	m.sort()

	result = []
	result.append(m[0][1])
	for x in xrange(1, len(m)):
		found = False
		for r in result:
			 if abs(m[x][1] - r) <= n:
				found = True
		if not found:
			result.append(m[x][1])
	result.sort()
	return result

def summary_index(blobs, pos):
        scores = [0 for x in xrange(len(blobs))]
        for i in xrange(len(blobs)):
                for j in xrange(i+1, len(blobs)):
                        sim = blob_similarity(str(blobs[i]), str(blobs[j]), pos)
                        scores[i] += sim
                        scores[j] += sim

        return scores.index(max(scores))

def select(arr, ind):
	result = []
	for i in ind:
		result.append(arr[i])
	return result

def create_tree(blobs, flow_pos, sum_pos, coeffs):
	base_indices = xrange(len(blobs))	
	parent_indices = [[-1,0] for x in xrange(len(blobs))]

	#for i in xrange(1):
	while True:
		print parent_indices
		nblobs = select(blobs, base_indices)
		m = minima(blob_flow(nblobs, flow_pos, coeffs), 2)
	
		summary_indices = []
		for i in xrange(0,len(m)-1):
			summary_indices.append(base_indices[m[i] + summary_index(select(nblobs, xrange(m[i], m[i+1])), sum_pos)])
			parent_indices[summary_indices[len(summary_indices)-1]][1] += 1
			for i in xrange(m[i], m[i+1]):
				parent_indices[base_indices[i]][0] = summary_indices[len(summary_indices)-1]

		if len(m) <= 2 or len(summary_indices) == 0:
			break

		base_indices = summary_indices
	print parent_indices
	
	summary_indices = []
	if len(base_indices) > 1:
		summary_indices.append(base_indices[summary_index(select(blobs, base_indices), sum_pos)])
		parent_indices[summary_indices[0]][1] += 1
		for i in xrange(len(base_indices)):
			parent_indices[base_indices[i]][0] = summary_indices[0]

	print parent_indices

	print "timeouts " + str(rb.timeouts)

	return parent_indices

def render(y, path):
    figure()
    plot(y, 'o-')
    xlabel("Sentence Number")
    ylabel("Correlation to previous flow")
    title("Segmentation of Article into Primary Thoughts")
    savefig(path)

def process_file(path, result):
	print rb.timeouts
	content = ""
	with open(path, 'r') as content_file:
		content = content_file.read()
	content = content.decode('utf-8').encode('ascii', 'ignore')
	sentences = TextBlob(content).sentences
#	render(convolute(blob_flow(sentences, "NN", [[1, 1], [2, 0.7], [3, 0.3], [4, 0.7], [5, .2]]), [.4, .4, .2]), result)
	render(blob_flow(sentences, "NN", [[1, 1], [2, 0.7], [3, 0.3], [4, 0.7], [5, .2]]), result)
	#print create_tree(sentences, "NN", "", [[1, 0.5], [2, 0.25], [3, 0.125], [4, 0.125]])
	print rb.timeouts

#process_file("/var/www/patch/test/data/article2.txt", "/var/www/patch/article2.png")
