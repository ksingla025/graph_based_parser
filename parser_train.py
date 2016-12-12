#!/usr/bin/python

import sys,os,commands,getopt
from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy as np
from random import shuffle

def train_classifier(input_file,model_name):
   print "Training classifier"
   X = []
   Y = []
   count = 0
   inp = open(input_file,'r').readlines()
   shuffle(inp)
   print "file shuffled"
   for i in range(0,len(inp)):
      inp[i] = inp[i].strip().split()
#      print line
#      print inp[i][0]
      Y.append(inp[i][0])
      X.append(inp[i][1:])
#      print len(inp[i][1:])
   y = np.array(Y)
   x = np.array(X)

   clf = SVC(probability=True)
   clf.fit(x, y)
   joblib.dump(clf, model_name+".pkl") 


def main(argv):
   inputfile = ''
   outputfile = ''
   wsize = ''
   vectorn = ''
   vectorm = ''
   try:
      opts, args = getopt.getopt(argv,"h:i:o:w:n:m:p:",["ifile=","ofile=","wsize=","vectn=","vectm=","pos="])
   except getopt.GetoptError:
      print 'parser_train.py -i <inputfile> -o <outputfile> -w <window_size> -n <vector_normal> -m <vector_main> -p <pos_flag>'
#      print 'test.py -i <inputfile> -o <outputfile>'
      print " -w(integer) is the context window you want to keep\n"
      print " -n(vectors) is the vector file for the words which don't get root position\n"
      print " -m(vectors) is the vector file for the words which get root position\n"
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h' or opt == '--help':
         print 'parser_train.py -i <inputfile> -o <outputfile> -w <window_size> -n <vector_normal> -m <vector_main>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-w", "--wsize"):
         wsize = arg
      elif opt in ("-n", "--vectn"):
         vectorn = arg
      elif opt in ("-m", "--vectm"):
         vectorm = arg
      elif opt in ("-p", "--pos"):
         pos = arg
   print 'Input file is :', inputfile
   print 'Output file is :', outputfile
   print 'wndow size is :', wsize
   print 'vector for normal :', vectorn
   print 'vector for main :', vectorm
   print 'Using POS :', pos

   print commands.getstatusoutput("python scripts/train/connl2word_pairs.py "+inputfile+" "+outputfile+" "+wsize)

   print "WORD PAIRS GENERATED"

   print commands.getstatusoutput("python scripts/train/wordpairs2svm.py "+outputfile+" "+vectorn+" "+vectorm)

   print "Training file generated"

   
   train_classifier("train_files/"+outputfile+".svm","train_files/"+outputfile+".model")
#   print commands.getstatusoutput("svm-train -b 1 temp/"+outputfile+".svm temp/"+outputfile+".model")
   
if __name__ == "__main__":
        main(sys.argv[1:])

