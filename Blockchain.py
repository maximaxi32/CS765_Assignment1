# importing libraries
import hashlib
import uuid

# importing other modules
import Latency
import Transaction
import Event
import Node
import Block


# class describing a blockchain
class Blockchain:
    # constructor
    def __init__(self, n):
        self.chain = dict()
        self.n = n
        self.genesisBlock = None
        self.createGenesisBlock()
        self.longestLength = 1
        self.farthestBlock = self.genesisBlock

    # function to get the block at the end of the longest chain
    def getLastBlock(self):
        return self.farthestBlock

    # function to create the genesis block
    def createGenesisBlock(self):
        self.genesisBlock = Block.GenesisBlock(0, self.n)
        self.chain[self.genesisBlock] = []

    # function to add a block to the blockchain after a given block
    def addBlock(self, block, prevBlock):
        self.chain[prevBlock].append(block)
        if self.chain.get(block) == None:
            self.chain[block] = []

    # function to return the block with a given hash
    def getBlock(self, hashSearch):
        for blk in self.chain:
            if str(blk.hash) == str(hashSearch):
                return blk
        return None
