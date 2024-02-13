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


    def createGenesisBlock(self):
        # Create the genesis block
        self.genesisBlock = Block.GenesisBlock(0,self.n)
        self.chain[self.genesisBlock]=[]

    def addBlock(self, block,prevBlock):
        # Add a new block to the chain
        block.previousHash = prevBlock.hash
        block.calculateHash()
        
        # if(self.chain.get(prevBlock)==None):
        #     self.chain[prevBlock]=[]
        self.chain[prevBlock].append(block)
        if self.chain.get(block)==None:
            self.chain[block]=[]

    def getBlock(self,hashSearch):

        #return self.genesisBlock
        for blk in self.chain:
            # print(blk.hash,hashSearch)
            if str(blk.hash)==str(hashSearch):
                # print(blk.BlkId)
                #print("found")
                return blk
        return None

