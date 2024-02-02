# importing libraries
import uuid
import datetime as dt
import numpy as np
import random
import math
# importing other modules
import Latency

# Class to store the Node
class Node:
    def __init__(self,expMean):
        self.Id = str(uuid.uuid4())
        self.neighbors = []
        self.balance = float(100)
        self.isSlow = False
        self.isLowCPU = False
        self.toSleep=1
        self.expMean=expMean

    def getID(self):
        return self.Id

    def setSlow(self, isSlow):
        self.isSlow = isSlow
        
    def getSlow(self):
        return self.isSlow

    def setLowCPU(self, isLowCPU):
        self.isLowCPU = isLowCPU
        
    def getLowCPU(self):
        return self.isLowCPU

    # Add one new neighbor to this node
    def addNeighbor(self, newNeighbor):
        self.neighbors.append(newNeighbor)

    # Return a list of node's neighbors
    def getNeighbors(self):
        return self.neighbors
    
    def generateTransaction(self,globalTime,ListOfPeers):
        if globalTime%self.toSleep==0:
            self.toSleep=math.ceil(np.random.exponential(self.expMean))
            yield self.printTransaction(ListOfPeers)
        yield self.getID() + " is Idle"
    
    def printTransaction(self,ListOfPeers):
        n=len(ListOfPeers)        #number of Nodes in network
        whomToSend=ListOfPeers[random.randint(0,n-1)]
        print(Latency.generateLatency(ListOfPeers))
        while whomToSend==self.Id:
            whomToSend=ListOfPeers[random.randint(0,n-1)]
        if self.balance>1:
            whatToSend=np.random.uniform(0,self.balance)
        else :
            return "TxnID: "+self.Id+" Insufficient Balance"
        self.balance-=float(whatToSend)
        return "TxnID: "+self.Id+" pays "+whomToSend.getID()+" "+str(whatToSend)+" coins"
         
    