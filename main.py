# importing libraries
import argparse
import random
from queue import PriorityQueue
import numpy as np
import math
import sys
import pydot
from dsplot.graph import Graph
from PIL import Image

# importing user modules
import Node
import Network
import Event
import Graph

rhoMatrix=[]

#setting up the input arguments parser
parser = argparse.ArgumentParser()



# This is the main function
# usage: main.py [-h] --n N --z0 Z0 --z1 Z1 --Tx TX --Itr ITR --Sim SIM
def main():
    # Parsing user arguments
    parser.add_argument("--n", type=int, required=True) #number of Nodes
    parser.add_argument("--z0", type=float, required=True)  #percentage of slow nodes
    parser.add_argument("--z1", type=float, required=True)  #percentage of low CPU nodes
    parser.add_argument("--Tx", type=float, required=True)  #mean time for interarrival Of Transactions
    parser.add_argument("--Itr", type=float, required=True) #mean time for interarrival of Blocks
    parser.add_argument("--Sim", type=float, required=True) #Total Simulation time

    args = parser.parse_args()
    n = args.n
    z0 = args.z0
    z1 = args.z1
    Tx = args.Tx    
    Itr = args.Itr  
    timeLimit = args.Sim
    
    
    eventQueue=PriorityQueue()            #Global Event Queue implemented with a min Priority Queue


    open('TxnLog.txt', 'w').close()        #Clearing the Transactions Log file



    # Initializing the list of peer nodes
    ListOfPeers = []
    for _ in range(0, n):
        newNode=Node.Node(n,Tx,_,Itr)
        ListOfPeers.append(newNode)
        newNode.rhos=[0]*n
        firstTxn=(np.random.exponential(Tx))    #Generating the first generateTransaction event for each Node
        eventQueue.put([firstTxn,Event.Event(newNode,firstTxn,None,"generateTransaction",ListOfPeers,eventQueue)])
       




    #Assigning isSlow and isLowCPU values to the Nodes
    assign_z0(ListOfPeers, z0, n)
    assign_z1(ListOfPeers, z1, n)

    #Generating the first mineBlock event for each Node
    for peer in ListOfPeers:
        firstMine=(np.random.exponential(Itr/peer.hashPower)/2)
        eventQueue.put([firstMine,Event.Event(peer,firstMine,peer.blockchain.genesisBlock,"mineBlock",ListOfPeers,eventQueue)])  

    #Create Network of peers
    Network.createNetwork(ListOfPeers)

    #create rho matrix
    rhoGenerator(ListOfPeers)



    genTxn = 0  # To keep track of number of generate Transaction events

    #Loop to simulate events from eventqueue   
    while 1:
        currEvent=eventQueue.get()[1]
        if(currEvent.timestamp>timeLimit):
            break
        if(currEvent.eventType=="generateTransaction"):
            genTxn+=1
        currEvent.execute(ListOfPeers,eventQueue)

  
    
    #Plotting the blockchain for all peers
    Graph.plotter(ListOfPeers)
  
   #Printing the stats for all peers

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    totalMined=0
    for peer in range(n):
        print("Stats for Node {} having isSlow={} and isLow={}".format(ListOfPeers[peer].idx,ListOfPeers[peer].isSlow,ListOfPeers[peer].isLowCPU))
        print("Number of Blocks mined:",ListOfPeers[peer].minedCnt)
        print("Number of Blocks received:",ListOfPeers[peer].receivedCnt)
        print("Length of longest chain in Blockchain:",ListOfPeers[peer].blockchain.farthestBlock.depth)
        totalMined+=ListOfPeers[peer].minedCnt

        
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Number of Generate Transaction Events: "+str(genTxn))
    print("Total number of Blocks Mined: ",totalMined)

    


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
    # hashPowerofLow * n * z1 + hashPowerofHigh * (n - (n * z1) = 1


    numTrues = int((z1 * n) / 100)
    labels = [True] * numTrues
    hashPowerofLow = 1*100 / (10 * n - 9 * numTrues)
    hashPowerofHigh = 10 * hashPowerofLow

    labelsFalse=[False] * (n - numTrues)
    labels+=labelsFalse
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setLowCPU(labels[_])
        if(labels[_] == True):
            ListOfPeers[_].setHashPower(hashPowerofLow/100)
        else:
            ListOfPeers[_].setHashPower(hashPowerofHigh/100)


def rhoGenerator(ListOfPeers):
    n=len(ListOfPeers)        #number of Nodes in network
    for i in range(n):
        for j in range(i):
            currentRho=np.random.uniform(0.01,0.5)
            ListOfPeers[i].rhos[ListOfPeers[j].idx]=currentRho
            ListOfPeers[j].rhos[ListOfPeers[i].idx]=currentRho

if __name__ == "__main__":
    main()
    