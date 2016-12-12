#!/usr/bin/python

import sys

conll = open(sys.argv[1],'r').readlines()
string = []
for i in range(0,len(conll)):
	if conll[i] != "\n":
		line = conll[i].split()

#		if line[7] == "root":
#			string.append("MAIN")
#		else:
		string.append(line[1].lower())
	else:
		print " ".join(string)
		string = []
