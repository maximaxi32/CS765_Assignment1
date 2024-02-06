# importing libraries
import argparse
import random
from queue import PriorityQueue
import numpy as np
import math

# importing other modules
import Node
import Network
import Event

parser = argparse.ArgumentParser()

rhoMatrix=[]

# This is the main function
# usage: python3 main.py --n N --z0 Z0 --z1 Z1
def main():
    # Parsing user arguments
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--z0", type=float, required=True)
    parser.add_argument("--z1", type=float, required=True)
    parser.add_argument("--Tx", type=float, required=True)
    args = parser.parse_args()
    n = args.n
    z0 = args.z0
    z1 = args.z1
    Tx = args.Tx

    eventQueue=PriorityQueue()            ####IMPORTANT####


    # Initializing the list of peer nodes
    ListOfPeers = []
    for _ in range(0, n):
        newNode=Node.Node(Tx,_)
        ListOfPeers.append(newNode)
        newNode.rhos=[0]*n
        eventQueue.put([0,Event.Event(newNode,0,None,"generateTransaction",ListOfPeers,eventQueue)])



    assign_z0(ListOfPeers, z0, n)
    assign_z1(ListOfPeers, z1, n)
    # Creating the network of nodes
    Network.createNetwork(ListOfPeers)


    rhoGenerator(ListOfPeers)


    numEvents=1000
    for num in range(numEvents):
        eventQueue.get()[1].execute(ListOfPeers,eventQueue)
    


# Function to assign isSlow to the Nodes
def assign_z0(ListOfPeers, z0, n):
    numTrues = int((z0 * n) / 100)
    labels = [True] * numTrues
    labelsFalse=[False] * (n - numTrues)
    labels+=labelsFalse
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setSlow(labels[_])


# Function to assign isLowCPU to the Nodes
def assign_z1(ListOfPeers, z1, n):
    numTrues = int((z1 * n) / 100)
    labels = [True] * numTrues
    labelsFalse=[False] * (n - numTrues)
    labels+=labelsFalse
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setLowCPU(labels[_])

def rhoGenerator(ListOfPeers):
    n=len(ListOfPeers)        #number of Nodes in network
    for i in range(n):
        for j in range(i):
            currentRho=np.random.uniform(0.01,0.5)
            ListOfPeers[i].rhos[ListOfPeers[j].idx]=currentRho
            ListOfPeers[j].rhos[ListOfPeers[i].idx]=currentRho

def generateLatency(ListOfPeers,i,j,msgSize):
    c=0
    if (not ListOfPeers[i].getSlow()) and (not ListOfPeers[j].getSlow()):
        c=100
    else :
        c=5
    #everything is in units of bits and seconds
    d=np.random.exponential(96*1000/(c*1000000))
    rho=rhoMatrix[i][j]
    latency=(rho)+(msgSize*1000*8/(c*1000000))+d
    return latency

if __name__ == "__main__":
    main()
    