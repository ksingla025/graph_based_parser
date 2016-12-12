#!/usr/bin/python

import sys,commands,os
from itertools import permutations
from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy as np
import operator
import itertools
import cPickle
from scripts.test.parse import *

''' takes an input file word-pair vectors, vector_file and returns output '''
def test_classifier(input_file,model_name,out_file):
	out = open(out_file,'w')
	clf = joblib.load(model_name)
	X = []
	for line in open(input_file,'r'):
		line = line.split()
		for i in range(1,len(line)):
			line[i] = line[i].split(":")[-1]
		X.append(line[1:])
	x = np.array(X)
	classes = clf.classes_
	out.write("labels "+" ".join(classes)+"\n")
	predicted = clf.predict_proba(x)
	
	for i in predicted:
		i = i.tolist()
		index, value = max(enumerate(i), key=operator.itemgetter(1))
		i = ['{:.6f}'.format(x) for x in i]
		i = " ".join(i)
		out.write(classes[index]+" "+i+"\n")

	out.close()

def perm_wordpairs(inp,wsize,temp_file):
	tokens = inp.split()
	tokens.reverse()
	tokens.append("MAIN")
	tokens.reverse()
	len1=len(tokens)
	perm = list(permutations(range(len1),2))
	for size in range(0,wsize):
		tokens.append("dummy")
		for size in range(0,wsize):
			tokens.reverse()
			tokens.append("dummy")
			tokens.reverse()

	out = open(temp_file,'w')
	for x in range(0,len(perm)):
		child = ''
		parent = ''
		for y in range(perm[x][0],perm[x][0]+wsize*2+1):
			if child != '':
				child = child +" " + tokens[y]
			else:
				child = tokens[y]
		for y in range(perm[x][1],perm[x][1]+wsize*2+1):
			if parent != '':
				parent = parent + " " + tokens[y]
			else:
				parent = tokens[y]
		out.write(parent+" "+child+" 1500\n")
	out.close()

def perm_prob(abv,prob_file):

	counter = 0
	out = open("test_files/"+abv+".temp",'r').readlines()
	out_prob = open(prob_file,'w')
	commands.getstatusoutput("python scripts/test/wordpairs2svm.py perm "+sys.argv[2])
	test_classifier("test_files/perm.svm",classifier_name,"test_files/perm.pre")
	perm = open("test_files/perm.pre",'r').readlines()
	labels = perm[0].split()[1:]
	maps = {}

	for x in range(0,len(labels)):
		counter = counter + 1
		if labels[x] == '999':
			root = counter
		maps[labels[x]] = counter

	out_prob.write("root "+inp[i])
	for j in range(1,len(perm)):
		pair = out[j-1].split()[:-1]
#		print pair
		if pair[-1-wsize] == "MAIN":
#			print "hello"
			prob = perm[j].split()[int(maps['999'])]
			label = '999'
#			print "hello"
#                               pair = pair[1]+" "+pair[0]
			out_prob.write(" ".join(pair)+" "+label+" "+prob+"\n")

		else:
			label = perm[j].split()[0]
#                             pair = pair[1]+" "+pair[0]
			out_prob.write(" ".join(pair)+" "+label+" "+perm[j].split()[int(maps[str(label)])]+"\n")

	out_prob.close()
#wsize = sys.argv[2] ### will be the same as kept in training

def mst2conll(mst):
	sent = mst[0]
	label_arc = mst[2]

	answer_dic = {}

	for key in label_arc.keys():
		for key2 in label_arc[key].keys():
			if key2 not in answer_dic.keys():
				answer_dic[key2] = {}

			answer_dic[key2][key] = label_arc[key][key2]
		#print answer_dic
#	print mst[1]
#	print answer_dic
	sent = sent.split()
	for key in answer_dic.keys():
		head = str(answer_dic[key].items()[0][0])
		label = str(answer_dic[key].items()[0][1])
		print str(key)+"\t"+sent[key]+"\t"+"_"+"\t_"+"\t_\t"+head+"\t"+label+"\t_\t_"



if __name__ == "__main__":

	inp_file = sys.argv[1] # test file with strings
	vector_file = sys.argv[2]
	classifier_name = sys.argv[3] #trained classifier pickle file
	wsize = int(sys.argv[4]) #size of context to be taken, same as model used
	labels = sys.argv[5] # label mapping file

	abv = "perm" 
	maps = {}
	inp = open(sys.argv[1],"r").readlines()
	commands.getstatusoutput("mkdir -p test_files")

	with open(labels, "rb") as input_file:
		label_mapping = cPickle.load(input_file)

	inv_map = {v: k for k, v in label_mapping.iteritems()}
#	print inv_map
	for i in range(0,len(inp)):
		
#		print "==> Processing Sentence "+str(i)
		perm_wordpairs(inp[i],wsize,"test_files/"+abv+".temp")

		perm_prob(abv,"test_files/"+abv+".prob")

		mst = file2mst("test_files/"+abv+".prob",inv_map)

		mst2conll(mst)

		print "\n",




		

			

