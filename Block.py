# importing libraries
import hashlib
import uuid
import datetime as dt
import numpy as np
import random
import math
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

        self.hash=str(hashlib.sha256((str(self.previous_hash) + self.BlkId + thash).encode()).hexdigest())

    def getHash(self):
        return self.hash        
        
    def addTransaction(self,txn):
        self.transactions.append(txn)
        self.size+=1

    def getsize(self):
        return self.size
    

class GenesisBlock():
    def __init__(self,timestamp,n):
        self.BlkId = str(1)
        self.timestamp=timestamp
        self.balances=[100000]*n
        self.hash=str(hashlib.sha256((str(self.BlkId).encode())).hexdigest())
        self.depth=1

    def getHash(self):
        return self.hash 

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
    

