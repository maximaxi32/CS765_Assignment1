# importing libraries
import random
from math import floor

# importing other modules
import Node


# To create a network of Peer Nodes
def createNetwork(ListofPeers):
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


# To check if the network is a connected graph or not
def isConnected(ListofPeers):
    # TODO: Implement BFS/DFS
    pass
