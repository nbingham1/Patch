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
import pydot as pydot

rb = RhineBundle()
rb.rhineGenerate('/var/www/patch/Rhine.txt')
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
                        #print word1[0]
                        #print word2[0]
                        try:
                            dist = rb.freshRhine().distance(word1[0],word2[0])
                            if math.isnan(dist):
                                dist = 0
                            else:
                                dist = 30/(dist+29)
                        except:
                            rb.timeouts += 1
                            dist = 0
                        #print dist
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


def path_similarity_flow(sentences, count, pos):
	y = []
        y.append(0)
        for i in xrange(1,len(sentences)):
		y.append(blob_path_similarity(sentences[i], sentences[i-1], count, pos))
	return y

def path_n_similarity_flow(sentences, count, pos, n):
	y = []
        for i in xrange(n):
            y.append(0)
        for i in xrange(n,len(sentences)):
	    y.append(blob_path_similarity(sentences[i], sentences[i-n], count, pos))
	return y

def rhine_n_similarity_flow(sentences, count, pos, n):
	y = []
        for i in xrange(n):
            y.append(0)
        for i in xrange(n,len(sentences)):
	    y.append(blob_rhine_similarity(sentences[i], sentences[i-n], count, pos))
        print "Rhine timeouts (dropped points): "
        print rb.timeouts
        return y

#Careful about the formatting of flows
#flows right now is a list of lists. The first n are similarity_flow 0 to n-1
#The next n are rhine_similarity_flow 0 to n-1.

def flow_fusion(flows, n):
    combo_flow = []
    #Don't use more ns than this. Seriously. 
    n_weights = [1, .7, .3, .7, .2, 0, 0, 0, 0, 0, 0, 0, 0]
    #This should add to 1, and be the length of the rolling ave
    conv_function = [.4, .4, .2]
    #Incorperate n_weights
    for i in xrange(len(flows[0])):
        temp = 0
        for j in xrange(len(flows)):
            temp += n_weights[j]*flows[j][i]
        combo_flow.append(temp)


    #Average
    for i in xrange(len(combo_flow)-len(conv_function)):
        preval = combo_flow[i]
        for j in xrange(len(conv_function)):
            combo_flow[i] += combo_flow[i+j]*conv_function[j]
        combo_flow[i] -= preval
    return combo_flow


def find_arguments(flow):
    args = [0]
    #Find all local minima
    for i in xrange(1, len(flow)-1):
        if (flow[i-1] - flow[i]> 0.0) and (flow[i+1]-flow[i]>0.0):
            args.append(i)
    args.append(len(flow))

    arglist = []
    last = -10
    for i in xrange(len(args)-1):
        if args[i] - last > 2:
            last = args[i]
            arglist.append(last)

    return arglist

#returns -1 if sent should be in its own cluster, and index into cluster if should be paired
def is_in_cluster(sent, clusters):
    dists = []
    rdists = []
    for i in xrange(len(clusters)):
        dists.append(blob_path_similarity(sent, clusters[i], 5, "NN"))
        rdists.append(blob_rhine_similarity(sent, clusters[i], 4, "NNP"))
    cum = []
    cur_max = 0
    max_idx = -1
    for i in xrange(len(dists)):
        temp = .6*dists[i]+.4*rdists[i]         #These are magic numbers.
        cum.append(temp)
        if temp > cur_max:
            cur_max = temp
            max_idx = i
    if cur_max > .3:        #This is the threshold for new cluster
        return max_idx
    else:
        return -1

def make_flow_data(sentences):
    rhine_dist = rhine_n_similarity_flow(sentences, 3, "NNP", 1)
    sents = []
    for n in [1,2,3]:
        sents.append(path_n_similarity_flow(sentences, 5, "NN", n))
    sents.append(rhine_dist)
    return sents


#Takes two lists of blobs, outputs an N lists of length M
def connection_matrix(blobs1, blobs2):
    conns = []
    for blob1 in blobs1:
        line = []
        for blob2 in blobs2:
            a = blob_path_similarity(blob1,blob2, 5, "NN")
            b = blob_rhine_similarity(blob1,blob2,4, "NNP")
            line.append(.6*a + .4*b)
        conns.append(line)
    return conns

def representative_blob(blobs, count, pos):
	scores = [0] * len(blobs)
        for i in xrange(len(blobs)):
                for j in xrange(i+1, len(blobs)):
                        sim = blob_path_similarity(blobs[i], blobs[j], count, pos)
                        scores[i] += sim
			scores[j] += sim
        
	return blobs[scores.index(max(scores))]

#0 is main signal, 1 is partitioned signal nouns, 2 is partitioned proper nouns
def plotter(flows, args, uid):

    figure()
    plot(flows[0], 'o-')
    xlabel("Sentence Number")
    ylabel("Correlation to previous flow")
    title("Segmentation of Article into Primary Thoughts (Fused signal)")
    for el in args:
        axvline(x=el, ymin=0, linewidth=1, color='r')
    savefig('/var/www/patch/'+str(uid)+'flow.png')

    figure()
    subplot(2,1,1)
    plot(flows[1], 'o-')
    ylabel("Correlation to previous flow")
    title("Part Of Speech Signal")

    plt.subplot(2, 1, 2)
    plot(flows[2], 'o-')
    xlabel("Sentence Number")
    ylabel("Correlation to previous flow")
    title("Proper Noun Signal") 
    savefig('/var/www/patch/'+str(uid)+'subplots.png')

def conn_grapher(dists):
    graph = pydot.Dot(graph_type='graph')
    nodes = []
    for i in xrange(len(dists[0])):
        nodes.append(pydot.Node(str(i+1)))
        graph.add_node(nodes[i])

    for i in xrange(len(dists[0])):
        for j in xrange(i,len(dists)):
            if i != j:
                graph.add_edge(pydot.Edge(nodes[i],nodes[j],label=str(dists[i][j])))
    
    graph.write_png('whee.png')
