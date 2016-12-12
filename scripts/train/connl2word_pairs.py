#!/usr/bin/python

# Author : Karan Singla

import sys,re,os,commands

commands.getstatusoutput("mkdir -p train_files") ## create temp folder if not there

inp = open(sys.argv[1],'r').readlines()   ## connl input file
out1 = open("train_files/"+sys.argv[2]+".n.temp",'w')  ## word_pairs for all except root
out2 = open("train_files/"+sys.argv[2]+".main.temp",'w') ## word_pairs for roots
wsize = int(sys.argv[3]) ## number of words in the context
line = []
rel = []
counter = 0
for num in range(0,len(inp)):
	if inp[num] != "\n":
		tokens = inp[num].split()
		if len(tokens) == 10:
			line += [tokens[1]]
			rel += [[tokens[-4],tokens[-3]]]
		else:
			counter = counter + 1
	else:
		for size in range(0,wsize):
			line.append("dummy")
		for size in range(0,wsize):
			line.reverse()
			line.append("dummy")
			line.reverse()

		for i in range(0,len(rel)):
			if int(rel[i][0]) != 0:
				rell = int(rel[i][0])-1
				out1.write(" ".join(line[i+wsize-wsize:i+wsize+wsize+1])+" "+" ".join(line[rell-wsize+wsize:rell+2*wsize+1])+" "+rel[i][1]+"\n")
			else:
				out2.write(" ".join(line[i+wsize-wsize:i+wsize+wsize+1])+" "+" ".join(line[i:i+wsize])+" MAIN "+" ".join(line[i+wsize+1:i+2*wsize+1])+" root\n")
		line = []
		rel = [] 
