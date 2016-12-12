#!/usr/bin/python

import sys,re,os

inp = open(sys.argv[1],'r').readlines()
line = []
for num in range(0,len(inp)):
	if inp[num] != "\n":
		tokens = inp[num].split()
		line += [tokens[1]]
	else: 
		print " ".join(line)
		line = []	
