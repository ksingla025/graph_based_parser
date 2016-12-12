#!/usr/bin/python

import os,commands,sys
import pickle

vect_dim = 200
path = "train_files/"+sys.argv[1]
vect = sys.argv[2]
vect_main = sys.argv[3] 
word_pairs_n = open(path+".n.temp",'r').readlines()
word_pairs_main = open(path+".main.temp",'r').readlines()
out1 = open(path+".n.words.temp",'w')
out2 = open(path+".main.words.temp",'w')

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
		if line[-1].strip() == 'root':
			print counter
	seq = "\n".join(line[:-1])
	out1.write(seq.lower()+"\n")
for i in range(0,len(word_pairs_main)):
#	print word_pairs_main[i]
        line = word_pairs_main[i].split()
        for i in range(0,len(line)):
        	if line[i] != "MAIN":
        		line[i] = line[i].lower()

        seq = "\n".join(line[:-1])
        out2.write(seq+"\n")

out1.close()
out2.close()

maps['root'] = 999
with open(path+".map", 'wb') as handle:
	pickle.dump(maps, handle)
commands.getstatusoutput("g++ scripts/train/vec.c")
commands.getstatusoutput("./a.out "+vect+" < "+path+".n.words.temp > "+path+".n.vectors.temp")
commands.getstatusoutput("./a.out "+vect_main+" < "+path+".main.words.temp > "+path+".main.vectors.temp")

wordm = open(path+".main.words.temp",'r').readlines()
vectn = open(path+".n.vectors.temp",'r').readlines()
vectmain = open(path+".main.vectors.temp",'r').readlines()

svm_n = open(path+".n.svm",'w')
svm_main = open(path+".main.svm",'w')

comb_vect = ''
print vec_len

## put the vectors in the right training format 
j = 0
for i in range(0,len(word_pairs_n)):
	comb_vect = []
	for k in range(j,j+vec_len):
		comb_vect = comb_vect + vectn[k].strip().split()
	j = j + vec_len
	comb_vect = " ".join(comb_vect)
	relation = word_pairs_n[i].split()[-1]
	rel_index = maps[relation.strip()]
	svm_n.write(str(rel_index)+" "+comb_vect+"\n")

## put the vectors in the right training format
j = 0
for i in range(0,len(word_pairs_main)):
	comb_vect = []
	for k in range(j,j+vec_len):
		if wordm[k].strip() == "MAIN":
			print "hello"
			vect = vectmain[j].strip().split()
		else:
			vect = vectmain[k].strip().split()
		comb_vect = comb_vect + vect
	j = j + vec_len
	comb_vect = " ".join(comb_vect)
	relation = word_pairs_main[i].split()[-1]
	rel_index = maps[relation.strip()]
	svm_main.write(str(rel_index)+" "+comb_vect+"\n")

svm_main.close()
svm_n.close()


svm_comb = open(path+".svm",'w')
svm_n = open(path+".n.svm",'r')
for line in svm_n:
	line = line.split()
	for i in range(1,len(line)):
		line[i] = line[i].split(":")[-1]
	svm_comb.write("\t".join(line)+"\n")	

svm_main = open(path+".main.svm",'r')
for line in svm_main:
	line = line.split()
	for i in range(1,len(line)):
		line[i] = line[i].split(":")[-1]
	svm_comb.write("\t".join(line)+"\n")

svm_comb.close()