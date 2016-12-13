#!/usr/bin/python

import sys
from operator import itemgetter

system = open(sys.argv[1],'r').readlines()
gold = open(sys.argv[2],'r').readlines()

total_arcs = 0
correct_arcs = 0
total_labels = 0
correct_labels = 0
total_sents = 0
confusion_table = {}
for i in range(0,len(system)):

	if system[i] == "\n":
		total_sents = total_sents + 1
	else:
		total_labels = total_labels + 1
		total_arcs = total_arcs + 1
		
		system_label = system[i].split()[6]
		gold_label = gold[i].split()[7]
		if gold_label not in confusion_table.keys():
			confusion_table[gold_label] = {}
		if system_label not in confusion_table[gold_label].keys():
			confusion_table[gold_label][system_label] = 0
		if system_label == gold_label:
			correct_labels = correct_labels + 1

		confusion_table[gold_label][system_label] = confusion_table[gold_label][system_label] + 1

		system_parent = system[i].split()[5]
		gold_parent = gold[i].split()[6]
		if system_parent == gold_parent:
			correct_arcs = correct_arcs + 1

print "Total correct arcs   : ", correct_arcs, float(correct_arcs)*100/float(total_arcs)
print "Total correct labels : ", correct_labels, float(correct_labels)*100/float(total_labels)
