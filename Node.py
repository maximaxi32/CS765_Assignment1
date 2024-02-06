# importing libraries
import uuid
import datetime as dt
import numpy as np
import random
import math
# importing other modules
import Latency
import Transaction
import Event

# Class to store the Node
class Node:
    def __init__(self,expMean,idx):
        self.Id = str(uuid.uuid4())
        self.neighbors = []
        self.isSlow = False
        self.isLowCPU = False
        self.toSleep=1
        self.expMean=expMean
        self.txnpool=[]
        self.idx=idx
        self.balance=1000
        self.rhos=[]
        
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


    # def firstTransaction(self,ListOfPeers):
    #     toSleep=math.ceil(np.random.exponential(self.expMean))
    #     firstTxn=Transaction.Transaction(self,0,ListOfPeers,"create")
    #     eventQ


    def generateTransaction(self,timestamp,ListOfPeers,eventQueue):
        n=len(ListOfPeers)        #number of Nodes in network
        whomToSend=ListOfPeers[random.randint(0,n-1)]
        indexwhomToSend=-1
        while ListOfPeers[indexwhomToSend].getID()==self.Id:
            indexwhomToSend=random.randint(0,n-1)
            whomToSend=ListOfPeers[indexwhomToSend]
        
        whatToSend=np.random.uniform(0,self.balance)
        if whatToSend<=1:
            print("Txn: "+self.Id+" has Insufficient Balance")
            return
        
        
        Txn = Transaction.Transaction(self.Id,whomToSend.getID(),timestamp,ListOfPeers,"transfer",whatToSend)
        Txn.printTransaction()
        self.txnpool.append(Txn)

        self.toSleep=(np.random.exponential(self.expMean))
        newtimestamp=timestamp+self.toSleep
        eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,None,"generateTransaction",ListOfPeers,eventQueue)])
        
        for neighbor in self.neighbors:
            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,1)
            eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,Txn,"receiveTransaction",ListOfPeers,eventQueue)])      
            
         
    def receiveTransaction(self,timestamp,Txn,ListOfPeers,eventQueue):
        if(Txn in self.txnpool):    #if the transaction is already in the pool, then ignore it
            return
        self.txnpool.append(Txn)
        for neighbor in self.neighbors:
            newtimestamp=timestamp+generateLatency(ListOfPeers,self.idx,neighbor.idx,1)
            eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,"receiveTransaction",ListOfPeers,eventQueue)])      

        