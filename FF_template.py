#! /usr/bin/env python

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


# Finds AUG path
def findAugPath(Gr,s,t):
    count = 0
    path = []
    visitedList = []
    queue = [s]
    parent = {}

    # Simple BFS for finding one path:
    while queue:
        count += 1
        currentVertex = queue.pop(0)
        visitedList.append(currentVertex)

        for adj in Gr.adj(currentVertex):

            # Continue only if there is still flow left on the edge
            if adj == t and Gr.W[currentVertex,t] > 0:
                parent[adj] = currentVertex
                lastVertex = adj

                while True:
                    path.insert(0,lastVertex)
                    lastVertex = parent[lastVertex]

                    if lastVertex == s:
                        path.insert(0,lastVertex)
                        return(path,count)

            if adj not in visitedList and Gr.W[(currentVertex, adj)] > 0:
                queue.append(adj)
                parent[adj] = currentVertex

    # If path doesn't exist between s -> t, then return empty list
    return ([], count)


# Calculate AUG flow from min flow and store it to graph data
def makeAugFlow(Gr,s,t,path):
    f = {}
    if not path:
        return f
    if path[0] != s:
        raise Exception("Path not from s")
    if path[-1] != t:
        raise Exception("Path not to t")
    u = s

    # Find smallest flow in one path
    cfp = Gr.W[(path[0], path[1])]
    for i in range(1, len(path)):
        flowAvailable = Gr.W[(path[i-1], path[i])]
        if flowAvailable < cfp:
            cfp = flowAvailable

    # Go through path and store minimal value into edges
    for i in range(1, len(path)):

        # Don't do anything if vertex is the starting vertex
        if path[i] == u:
            continue
        
        # This saves cfp and negative cfp values into graph
        f[(path[i-1], path[i])] = cfp
        f[(path[i], path[i-1])] = -cfp

    return f


def fordFulkerson(G,s,t):
    # Count is a counter to see how many edges are processed in total
    count = 0
    f = {}
    pp = findAugPath(G,s,t)
    p = pp[0]
    count += pp[1]
    fp = makeAugFlow(G,s,t,p)
    f = sumFlow(f,fp)
    Gr = makeResidual(G,f)
    i = 0

    while p and i < 1000:
        i += 1
        pp = findAugPath(Gr,s,t)
        p = pp[0]
        count += pp[1]
        fp = makeAugFlow(Gr,s,t,p)
        f = sumFlow(f,fp)
        Gr = makeResidual(G,f)

    print("BFS vertex count: " + str(count))
    return f


# Simple function that makes testing easier
def calculateMaxFlow(graph, set):
    G = Graph(graph)
    S = readNodes(set)
    s, t = S
    f = fordFulkerson(G,s,t)

    maxflow = 0
    
    # Sums tota flow from the starting vertex into maxFlow
    for i in f:
        if(i[0]) == s:
            maxflow += f[i]

    print("Network's max flow: " + str(maxflow))


# Run this if this file is being run
if __name__ == "__main__":

    print("--\nRunning the simple test scenarios: \n-- \n")

    for i in ["1","2","3","4","5"]:
        print("Simple test " + i + ": ")
        calculateMaxFlow("testdata/test_flow_simple_" + i, "testdata/testset_simple_" + i)
        print()

    print("--\nRunning the normal test scenarios: \n -- \n")

    for i in ["10","100","1000","10000"]:
        print("Test " + i + ": ")
        calculateMaxFlow("testdata/testflow_" + i, "testdata/testset_" + i)
        print()
    