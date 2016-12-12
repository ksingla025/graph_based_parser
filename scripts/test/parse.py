import my_edmonds,sys,math
import itertools
from scripts.test.my_edmonds import *
#print perms
#print perms

def popmin(pqueue):
    # A (ascending or min) priority queue keeps element with
    # lowest priority on top. So pop function pops out the element with
    # lowest value. It can be implemented as sorted or unsorted array
    # (dictionary in this case) or as a tree (lowest priority element is
    # root of tree)
    lowest = 1000
    keylowest = None
    for key in pqueue:
        if pqueue[key] < lowest:
            lowest = pqueue[key]
            keylowest = key
    del pqueue[keylowest]
    return keylowest
 
def prim(graph, root):
    pred = {} # pair {vertex: predecesor in MST}
    key = {}  # keep track of minimum weight for each vertex
    pqueue = {} # priority queue implemented as dictionary
 
    for v in graph:
        pred[v] = -1
        key[v] = 1000
    key[root] = 0
    for v in graph:
        pqueue[v] = key[v]
     
    while pqueue:
        u = popmin(pqueue)
        for v in graph[u]: # all neighbors of v
            if v in pqueue and graph[u][v] < key[v]:
                pred[v] = u
                key[v] = graph[u][v]
                pqueue[v] = graph[u][v]
    return pred

def file2mst(file,label_mapping):
    f=open(file).readlines()
    perms=list(itertools.permutations(range(len(f[0].split())),2))
    graph={}
    graph[0] = {}
    edge_mapping = {}
    mst_mapping = {}
    i=0
#    print len(perms),len(f)

    for line in f[1:]:
        spl=line.split()
        if perms[i][1] == 0:
            i+=1
        else:
            if perms[i][0] not in graph.keys():
                graph[perms[i][0]] = {}
            if perms[i][0] not in edge_mapping.keys():
                edge_mapping[perms[i][0]] = {}
            if perms[i][0] == 0:
                edge_mapping[0][perms[i][1]] = label_mapping[int(spl[-2])]
                graph[0][perms[i][1]] = 0.0 - float(spl[-1])
            else:
                edge_mapping[perms[i][0]][perms[i][1]] = label_mapping[int(spl[-2])]
                graph[perms[i][0]][perms[i][1]] = 0.0 - float(spl[-1])
#            graph[perms[i][1]][perms[i][0]] = 0-math.log(float(spl[-1])*100)
            i+=1

#    print graph

    '''
    summ=0
    len1=len(f[0].split())-1
    for i in graph[len1]:
        summ+=graph[len1][i]
    for i in graph[len1]:
        graph[len1][i]=graph[len1][i]/summ


    min_ind=1
    minn=graph[0][1]
    for i in graph[0]:
        if graph[0][i]<minn:
            minn=graph[0][i]
            min_ind=i
    for i in graph[0]:
        if i!=min_ind:
            graph[0][i]/=100

#    for key in graph.keys():
#        print len(graph[key].keys())

    '''
#   del graph[0]
#    print graph
#   pred = prim(graph, 0)
#   for v in pred: print "%s: %s" % (v, pred[v])
    mst=my_edmonds.mst(0,graph)

    for key in mst.keys():
        for key2 in mst[key].keys():
            if key not in mst_mapping.keys():
                mst_mapping[key] = {}
            mst_mapping[key][key2] = edge_mapping[key][key2]
    return f[0],mst,mst_mapping
#   spl=f[0].split()

if __name__ == "__main__":
    print file2mst(sys.argv[1])
#print mst
