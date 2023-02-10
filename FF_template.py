#! /usr/bin/env python

# This file contains a template for the Ford-Fulkerson algorithm. 

from graafi3 import Graph
from copy import deepcopy as copy

# Read a set containing vertices.
def readNodes(filename):
    ff = open(filename,'r')
    x = ff.readlines()[0].split()
    S = []
    for i in x:
        S.append(int(i))
    return S

# Add the flows in f1 and f2.
def sumFlow(f1,f2):
    f = copy(f1)
    for (u,v) in f2:
        if not (u,v) in f:
            f[(u,v)] = f2[(u,v)]
        else:
            f[(u,v)] += f2[(u,v)]
    return f


# Form the residual network.
def makeResidual(G,f):
    Gr = copy(G)
    for (u,v) in f:
        c = 0
        # Copy the weight
        if (u,v) in Gr.W:
            c = Gr.W[(u,v)]
        # calculate residual capasity
        cf = c - f[(u,v)]
        if not v in Gr.AL[u]:
            Gr.addEdge(u,v)
        Gr.W[(u,v)] = cf
    return Gr

# This function is not complete. You must provide code to make it work properly.
def findAugPath(Gr,s,t):
    aug = []
    # laskuri is a counter to see how many edges are processed in total
    count = 0
    # Check to see whether s and t are adjacent.

    # BFS ?????
    path = []
    queue = [s]
    parent = {}
    visited = list()

    while queue:
        count += 1
        currentNode = queue.pop(0)
        visited.append(currentNode)

        for adj in Gr.adj(currentNode):
            if adj == t and Gr.W[currentNode,t] > 0:
                parent[adj] = currentNode
                previousInPath = adj

                while True:
                    path.insert(0,previousInPath)
                    previousInPath = parent[previousInPath]
                    if previousInPath == s:
                        path.insert(0,previousInPath)
                        return(path,count)

            if adj not in visited and Gr.W[(currentNode, adj)] > 0:
                queue.append(adj)
                parent[adj] = currentNode

    return ([], count)

# This is only a template, and does not work. You must complete it to make it work.
def makeAugFlow(Gr,s,t,path):
    f = {}
    if not path:
        return f
    if path[0] != s:
        raise Exception("Path not from s")
    if path[-1] != t:
        raise Exception("Path not to t")
    u = s
    # This is the minimum capacity on the path. You must find it!


    # print(Gr.W)
    min = Gr.W[(path[0], path[1])]
    print(min)
    for i in range(1, len(path)):
        flowAvailable = Gr.W[(path[i-1], path[i])]
        # print("flow available: " + str(flowAvailable))
        if flowAvailable < min:
            min = flowAvailable

    cfp = min
    #
    # Tahan tarvitaan implementaatio cfp:n laskemiselle

    # CFP = Flow's amount 
    #print("Min flow: " + str(cfp))
    #
    print(path)

    #for i in range(1, len(path)):
    #    f[(u,path[i])] = cfp
    #    f[(path[i],u)] = -cfp


    #print(f)

    for i in range(1, len(path)):
        if path[i] == u:
            continue
        
        f[(path[i-1], path[i])] = cfp
        f[(path[i], path[i-1])] = -cfp

    return f
    
def fordFulkerson(G,s,t):
    # laskuri is a counter to see how many edges are processed in total
    laskuri = 0
    f = {}
    pp = findAugPath(G,s,t)
    p = pp[0]
    laskuri += pp[1]
    fp = makeAugFlow(G,s,t,p)
    f = sumFlow(f,fp)
    Gr = makeResidual(G,f)
    i = 0
    while p and i < 1000:
        i += 1
        pp = findAugPath(Gr,s,t)
        p = pp[0]
        laskuri += pp[1]
        fp = makeAugFlow(Gr,s,t,p)
        f = sumFlow(f,fp)

        #print("fp: " + str(fp))
        #print("f: " + str(f))

        Gr = makeResidual(G,f)

    sum = 0
    for i in f.keys():
        if i[0] == 5:
            sum += f[i]
    print("Max flow: " + str(sum))

    print("Laskuri laski: " + str(laskuri))
    return f
        
if __name__ == "__main__":
    G = Graph("testdata/testflow_10")
    S = readNodes("testdata/testset_10")

    G = Graph("testdata/testflow_10")
    S = readNodes("testdata/testset_10")

    # print(S)
    s = S[0]
    t = S[1]
    f = fordFulkerson(G,s,t)

    maxflow = 0

    for i in f:
        if(i[0]) == s:
            maxflow += f[i]
            # print(str(i) + " - " + str(f[i]))

    print("Network's max flow: " + str(maxflow))