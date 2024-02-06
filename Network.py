# importing libraries
import random
from math import floor
import numpy as np
# importing other modules
import Node

rhoMatrix = []  # matrix to store the rho values between nodes

# To create a network of Peer Nodes
def createNetwork(ListofPeers):

    # To ensure finite attempts
    attempts = 0  # number of attempts to create a connected network
    

    # generate a new P2P network
    for _ in range(0, len(ListofPeers)):

        # if(attempts>100):
        #     print("Could not generate a connected network, take a larger N") 
        #     return
        # attempts+=1

        numOfNeighbors = random.randint(3, 6) - len(ListofPeers[_].getNeighbors())
        if numOfNeighbors <= 0:
            continue

        while numOfNeighbors > 0:
            newNeighborIdx = random.randint(0, len(ListofPeers) - 1)
            # print(str(_) + " --> " + str(newNeighborIdx))

            newNeighbor = ListofPeers[newNeighborIdx]
            if (
                (newNeighbor not in ListofPeers[_].getNeighbors())
                and (newNeighbor.getID() != ListofPeers[_].getID())
                and (len(newNeighbor.getNeighbors()) < 6)
            ):
                # Adding bidirectional edges for neighbors
                ListofPeers[_].addNeighbor(newNeighbor)
                newNeighbor.addNeighbor(ListofPeers[_])
                numOfNeighbors -= 1

    # check if the generated P2P network is connected or not
    if isConnected(ListofPeers) == False:
        for _ in range(0, len(ListofPeers)):
            ListofPeers[_].neighbors = []
            print("Issue: Generated network is disconnected")
    else:
        print("Generated a connected network!")

    #rhoGenerator(ListofPeers)
    #print(rhoMatrix)


# To check if the network is a connected graph or not
def isConnected(ListOfPeers):
    if not ListOfPeers:
        return True
    visited = set()
    start_node = ListOfPeers[0]
    dfs(start_node, visited)
    return len(visited) == len(ListOfPeers)


def dfs(node, visited):
    visited.add(node)
    currNeighbors = node.getNeighbors()
    for neighbor in currNeighbors:
        if neighbor not in visited:
            dfs(neighbor, visited)


def rhoGenerator(ListOfPeers,rhoMatrix):
    n=len(ListOfPeers)        #number of Nodes in network
    for i in range(n):
        for j in range(i):
            currentRho=np.random.uniform(0.01,0.5)
            rhoMatrix[ListOfPeers[i].idx][ListOfPeers[j].idx]=currentRho
            rhoMatrix[ListOfPeers[j].idx][ListOfPeers[i].idx]=currentRho

def rhoValue(i,j):
    return rhoMatrix[i][j]