# importing libraries
import hashlib
import uuid
import datetime as dt
import numpy as np
import random
import math
import copy
# importing other modules
import Latency
import Transaction
import Event
import Node


class Block():
    def __init__(self, previous_hash,timestamp,owner,depth):
        self.previous_hash = previous_hash
        self.BlkId = str(uuid.uuid4())
        self.timestamp=timestamp
        self.transactions=[]
        self.balances=[]
        self.owner=owner
        self.hash=""
        self.size=0
        self.depth=depth

    def calculateHash(self):
        thash=""
        for txn in self.transactions:
            thash+=txn.ID

        self.hash=str(hashlib.sha256(str(self.previous_hash).encode() + str(self.BlkId).encode() + str(thash).encode()).hexdigest())

    def getHash(self):
        return self.hash        
        
    def addTransaction(self,txn):
        self.transactions.append(txn)
        self.size+=1

    def getsize(self):
        return self.size

    def deepCopyBlk(self):
        copyOfBlk = Block(self.previous_hash,self.timestamp,self.owner,self.depth)
        

        copyOfBlk.previous_hash = self.previous_hash
        copyOfBlk.BlkId = self.BlkId
        copyOfBlk.timestamp = self.timestamp
        copyOfBlk.transactions = []
        copyOfBlk.balances = []
        for txn in self.transactions:
            copyOfBlk.transactions.append(txn)
        for bal in self.balances:
            copyOfBlk.balances.append(bal)
        copyOfBlk.owner = self.owner
        #copyOfBlk.calculateHash()
        copyOfBlk.hash = self.hash
        copyOfBlk.size = self.size
        copyOfBlk.depth = self.depth
        return copyOfBlk
    

class GenesisBlock():
    def __init__(self,timestamp,n):
        self.BlkId = str(1)
        self.timestamp=timestamp
        self.balances=[100000]*n
        self.hash=str(hashlib.sha256((str(self.BlkId).encode())).hexdigest())
        self.depth=1

    def getHash(self):
        return self.hash 
    
    def deepCopyBlk(self):
        copyOfBlk = GenesisBlock(self.timestamp,0)
        copyOfBlk.BlkId = self.BlkId
        copyOfBlk.timestamp = self.timestamp
        copyOfBlk.balances =[]
        for bal in self.balances:
            copyOfBlk.balances.append(bal)
        copyOfBlk.hash = self.hash
        copyOfBlk.depth = self.depth
        return copyOfBlk

#unit Testing

# def main():
#     ListOfPeers=[]
#     for _ in range(0, 5):
#         ListOfPeers.append(Node.Node(5,0))
#     gen=Block("0",0,1)

#     txn=Transaction.Transaction(ListOfPeers[1].getID(),ListOfPeers[1].getID(),0,ListOfPeers,"coinbase",50)
#     gen.addTransaction(txn)
#     for i in range(10):
#         txn=Transaction.Transaction(ListOfPeers[random.randint(0,4)],ListOfPeers[random.randint(0,4)],i,ListOfPeers,"transfer",random.randint(1,100))

#         gen.addTransaction(txn)
#     genblock=GenesisBlock(0,ListOfPeers)
#     print(genblock.hash)
    

