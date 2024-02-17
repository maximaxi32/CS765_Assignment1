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
import Block



class Blockchain():
    def __init__(self, n):
        self.chain = dict()
        # self.ListOfPeers = ListOfPeers
        self.n=n
        self.genesisBlock=None
        self.createGenesisBlock()
        self.longestLength=1
        self.farthestBlock=self.genesisBlock

    def getLastBlock(self):
        return self.farthestBlock
        

    def createGenesisBlock(self):
        # Create the genesis block
        self.genesisBlock = Block.GenesisBlock(0,self.n)
        self.chain[self.genesisBlock]=[]
       

    def addBlock(self, block, prevBlock):
        # Add a new block to the chain
        self.chain[prevBlock].append(block)
        if self.chain.get(block)==None:
            self.chain[block]=[]

    def getBlock(self,hashSearch):

        for blk in self.chain:
            if str(blk.hash)==str(hashSearch):
                return blk
        return None

