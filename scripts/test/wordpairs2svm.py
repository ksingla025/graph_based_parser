#!/usr/bin/python

import os,commands,sys

vect_dim = 50

home_path = "/Users/Singla/Desktop/projects/parser"
path = home_path+"/test_files/"+sys.argv[1]
vect = sys.argv[2]
word_pairs_n = open(path+".temp",'r').readlines()
out1 = open(path+".words.temp",'w')

wsize = (len(word_pairs_n[0].split(" "))-3)/4
vec_len = len(word_pairs_n[0].split(" "))-1

rel = []
maps = {}
counter = 0
for i in range(0,len(word_pairs_n)):
	line = word_pairs_n[i].split(" ")
	if line[-1].strip() not in rel:
		counter = counter + 1
		rel += [line[-1].strip()]
		maps[line[-1].strip()] = counter
	seq = "\n".join(line[:-1])
	out1.write(seq+"\n")

out1.close()
print rel
print maps
commands.getstatusoutput("g++ "+home_path+"scripts/train/vec.c")
commands.getstatusoutput(home_path+"/a.out "+vect+" < "+path+".words.temp > "+path+".vectors.temp")

vectn = open(path+".vectors.temp",'r').readlines()
wordn = open(path+".words.temp",'r').readlines()
svm_n = open(path+".svm",'w')

j = 0	
#print vec_len
for i in range(0,len(word_pairs_n)):
	comb_vect = []
	for k in range(j,j+vec_len):
		if wordn[k].strip() == "MAIN":
			print "hello"
			vect = vectn[j].strip().split()
		else:
			vect = vectn[k].strip().split()
		comb_vect = comb_vect + vect
#	print j
	j = j + vec_len
	comb_vect = " ".join(comb_vect)
#	print comb_vect
	relation = word_pairs_n[i].split()[-1]
	rel_index = maps[relation.strip()]
	svm_n.write(str(rel_index)+" "+comb_vect+"\n")

