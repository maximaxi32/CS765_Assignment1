# importing libraries
import argparse
import random
from queue import PriorityQueue
import numpy as np
import math
import sys
from dsplot.graph import Graph
sys.setrecursionlimit(100000)

# importing other modules
import Node
import Network
import Event
import Graph
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
    parser.add_argument("--Itr", type=float, required=True)

    args = parser.parse_args()
    n = args.n
    z0 = args.z0
    z1 = args.z1
    Tx = args.Tx    #ideal value = 1
    Itr = args.Itr  #ideal value = 1000

    eventQueue=PriorityQueue()            ####IMPORTANT####


    # Initializing the list of peer nodes
    ListOfPeers = []
    for _ in range(0, n):
        newNode=Node.Node(n,Tx,_,Itr)
        ListOfPeers.append(newNode)
        newNode.rhos=[0]*n
        firstTxn=(np.random.exponential(Tx))
        eventQueue.put([firstTxn,Event.Event(newNode,firstTxn,None,"generateTransaction",ListOfPeers,eventQueue)])
        firstMine=(np.random.exponential(Itr))
        #firstMine=0
        eventQueue.put([firstMine,Event.Event(newNode,firstMine,newNode.blockchain.genesisBlock,"mineBlock",ListOfPeers,eventQueue)])  




    assign_z0(ListOfPeers, z0, n)
    assign_z1(ListOfPeers, z1, n)

    Network.createNetwork(ListOfPeers)


    rhoGenerator(ListOfPeers)


    numEvents=100
    eventCount=0
    mineCount=0
    genTxn = 0
    timeLimit=100 # 10 seconds
    while 1:
        
        # eventQueue.get()[1].execute(ListOfPeers,eventQueue)
        currEvent=eventQueue.get()[1]
        #if(currEvent.eventType=="mineBlock"):
            # print(currEvent.owner.idx)
        #print(currEvent.timestamp)
        if(currEvent.timestamp>timeLimit):
            break
        # if  currEvent.eventType=="mineBlock" or currEvent.eventType=="generateTransaction":
        #     eventCount+=1
        if(currEvent.eventType=="generateTransaction"):
            genTxn+=1
        if  currEvent.eventType=="mineBlock":
            mineCount+=1
            # print(currEvent.timestamp)
        # print(currEvent.timestamp,currEvent.eventType)
            # print(currEvent.eventType)
        currEvent.execute(ListOfPeers,eventQueue)
    
    print("Number of Transactions Generated: "+str(genTxn))
    print("Number of Blocks Mined: "+str(mineCount))
    plotter=dict()


    Graph.plotter(ListOfPeers)
    # mapper={"1":["2"],[]}
    # graph1=Graph(mapper,directed=True)
    # graph1.plot()    

    #PLOTTING

    #print("length of node "+str(len(ListOfPeers[0].blockchain.chain))) 
    
    # for key in ListOfPeers[4].blockchain.chain:
    #     if plotter.get(int(hash(key.BlkId)))==None:
            
    #         plotter[int(hash(key.BlkId))]=[]
    #     for neighbor in ListOfPeers[4].blockchain.chain[key]:
            
    #         plotter[int(hash(key.BlkId))].append(int(hash(neighbor.BlkId)))
    #         if plotter.get(int(hash(neighbor.BlkId)))==None:
    #             plotter[int(hash(neighbor.BlkId))]=[]
    # print(len(plotter))
    # graph=Graph(plotter,directed=True)
    # graph.plot(fill_color='darkorchid')


    for peer in range(n):
        
        # print(ListOfPeers[peer].blockchain.longestLength)
        # temp=-1
        # for key in ListOfPeers[peer].blockchain.chain:
        #     if(key.BlkId!="1"):
        #         pass
        #         #print(ListOfPeers[peer].Id,key.owner)
        #     #temp=max(temp,key.depth)
        #     for block in ListOfPeers[peer].blockchain.chain[key]:
        #         pass
        
        # print(temp,ListOfPeers[peer].blockchain.longestLength)
                # print(block.owner)
        #     print()
            #print(str(key.BlkId)+" "+str(len(ListOfPeers[peer].blockchain.chain[key])))
        # print(len(ListOfPeers[peer].blockchain.chain))
    # for txn in ListOfPeers[2].txnpool:
    #     print(txn.sender)
    # for peer in ListOfPeers:
    #     print(len(peer.txnpool))
        print((len(ListOfPeers[peer].blockchain.chain[ListOfPeers[peer].blockchain.genesisBlock])))
        print(ListOfPeers[peer].minedCnt)
        print("~~~~~~~~~~~")
    # print(len(ListOfPeers[0].blockchain.chain))
    


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

    # Equations:
    # hashPowerofLow * numTrues + hashPowerofHigh * (n - numTrues) = 1
    # hashPowerofHigh = 10 * hashPowerofLow

    hashPowerofLow = 1*100 / (10 * n - 9 * numTrues)
    hashPowerofHigh = 10 * hashPowerofLow

    labelsFalse=[False] * (n - numTrues)
    labels+=labelsFalse
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setLowCPU(labels[_])
        if(labels[_] == True):
            ListOfPeers[_].setHashPower(hashPowerofLow)
        else:
            ListOfPeers[_].setHashPower(hashPowerofHigh)


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
    