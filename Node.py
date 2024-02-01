# importing libraries
import uuid
import datetime as dt

# importing other modules


# Class to store the Node
class Node:
    def __init__(self):
        self.Id = str(uuid.uuid4())
        self.neighbors = []
        self.balance = float(10)
        self.isSlow = False
        self.isLowCPU = False

    def getID(self):
        return self.Id

    def setSlow(self, isSlow):
        self.isSlow = isSlow

    def setLowCPU(self, isLowCPU):
        self.isLowCPU = isLowCPU

    # Add one new neighbor to this node
    def addNeighbor(self, newNeighbor):
        self.neighbors.append(newNeighbor)

    # Return a list of node's neighbors
    def getNeighbors(self):
        return self.neighbors
    
    def generateTransaction(self,ListOfPeers):
        n=len(ListOfPeers)        #number of Nodes in network
        whomToSend=ListOfPeers[random.randint(0,n-1)]
        while whomToSend==self.Id:
                whomToSend=ListOfPeers[random.randint(0,n-1)]
        whatToSend=random.randint(1,self.balance)
        self.balance-=whatToSend
        return "TxnID:"+self.Id+" pays "+whomToSend+" "+str(whatToSend)+" coins"
         
    