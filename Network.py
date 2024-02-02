# importing libraries
import random
from math import floor

# importing other modules
import Node


# To create a network of Peer Nodes
def createNetwork(ListofPeers):
    # generate a new P2P network
    for _ in range(0, len(ListofPeers)):
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