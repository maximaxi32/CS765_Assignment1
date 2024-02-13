# importing libraries
import uuid
import datetime as dt
import numpy as np
import random
import math
from dsplot.graph import Graph
# importing other modules
import Latency
import Transaction
import Event
import Block
import Blockchain

# Class to store the Node
class Node:
    def __init__(self,n,expMean,idx,interArrival):
        self.Id = str(uuid.uuid4())
        self.neighbors = []
        self.isSlow = False
        self.isLowCPU = False
        self.toSleep=1
        self.expMean=expMean
        self.txnpool=[]
        self.verifiedPool=[]
        self.idx=idx
        self.hashPower=0
        self.tkMean=0
        self.rhos=[]
        self.pending=[]
        self.invalid=[]
        self.blockchain=Blockchain.Blockchain(n)
        self.interArrival=interArrival
        
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
    
    def setHashPower(self,hashPower):
        self.hashPower=hashPower
        self.tkMean=(self.interArrival)/hashPower

    # def firstTransaction(self,ListOfPeers):
    #     toSleep=math.ceil(np.random.exponential(self.expMean))
    #     firstTxn=Transaction.Transaction(self,0,ListOfPeers,"create")
    #     eventQ


    def generateTransaction(self,timestamp,ListOfPeers,eventQueue):
        n=len(ListOfPeers)        #number of Nodes in network
        whomToSend=ListOfPeers[random.randint(0,n-1)]
        indexwhomToSend=self.idx
        while ListOfPeers[indexwhomToSend].getID()==self.Id:
            indexwhomToSend=random.randint(0,n-1)
            whomToSend=ListOfPeers[indexwhomToSend]
        
        # whatToSend=np.random.uniform(0,self.balance/10)
        whatToSend=np.random.uniform(1,1000)  #ideal case

        if whatToSend<=1:
            print("Txn: "+self.Id+" has Insufficient Balance")
            return
        
        
        Txn = Transaction.Transaction(self.Id,whomToSend.getID(),timestamp,ListOfPeers,"transfer",whatToSend)
        Txn.printTransaction("transfer")
        self.txnpool.append(Txn)

        self.toSleep=(np.random.exponential(self.expMean))
        newtimestamp=timestamp+self.toSleep
        eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,None,"generateTransaction",ListOfPeers,eventQueue)])
        
        # if(Txn.type=="coinbase"):
        #     print(Txn.sender, Txn.receiver)

        for neighbor in self.neighbors:
            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,1)
            eventQueue.put([newtimestamp,Event.Event(neighbor,newtimestamp,Txn,"receiveTransaction",ListOfPeers,eventQueue)])      
            
         
    def receiveTransaction(self,timestamp,Txn,ListOfPeers,eventQueue):
        #print(self.Id,Txn.sender)
        if((Txn in self.txnpool) or (Txn in self.verifiedPool)): 
            return   #if the transaction is already in the pool, then ignore it
        self.txnpool.append(Txn)
        # print(self.Id,Txn.sender)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(str(self.Id)+" ~ "+str(Txn.sender))    

        
        # if(self.idx==0):
        #     print(Txn.sender)
            #   or (Txn in self.verifiedPool)
        
        for neighbor in self.neighbors:
            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,1)
            eventQueue.put([newtimestamp,Event.Event(neighbor,newtimestamp,Txn,"receiveTransaction",ListOfPeers,eventQueue)])      

    def mineBlock(self,timestamp,prevBlock,ListOfPeers,eventQueue):
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #print(len(self.txnpool))
        # print(prevBlock.depth)
        # print(self.blockchain.longestLength)
        if prevBlock.depth<self.blockchain.longestLength:   # POINT OF FAILURE
            return
        
        if len(self.txnpool)==0:
            #adding the event to mine the next block
            nextMine=(np.random.exponential(self.tkMean))
            newtimestamp=timestamp+nextMine
            eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,prevBlock,"mineBlock",ListOfPeers,eventQueue)])
            return

            
        newBlock=Block.Block(prevBlock.getHash(),timestamp,self.getID(),prevBlock.depth+1)
        self.blockchain.longestLength = max(self.blockchain.longestLength,prevBlock.depth+1)
        #Adding coinbase transaction
        coinbasetxn=Transaction.Transaction(self.getID(),self.getID(),timestamp,ListOfPeers,"coinbase",50)
        newBlock.addTransaction(coinbasetxn)
        coinbasetxn.printTransaction("coinbase")

       
        currBalances=prevBlock.balances.copy()    #create a balance copy
        newBlock.balances=currBalances    #Added this to prevent balances from going NULL
        for txn in self.txnpool:
            if newBlock.size>=950:
                break
            senderIdx=-1
            receiverIdx=-1
            # To get the indices of sender and receiver
            for peer in ListOfPeers:
                if peer.getID()==txn.sender:
                    senderIdx=peer.idx
                if peer.getID()==txn.receiver:
                    receiverIdx=peer.idx
            # To verify the transaction
            # if txn.type=="coinbase":
            #     txn.printTransaction("coinbase")
            #     currBalances[senderIdx]+=txn.amount
            #     self.txnpool.remove(txn)
            #     self.verifiedPool.append(txn)                 
            #     continue
            
            if currBalances[senderIdx]>=txn.amount:
                # print(senderIdx,end=" ")
                # print("amount "+str(txn.amount))
                currBalances[senderIdx]-=txn.amount
                currBalances[receiverIdx]+=txn.amount
                newBlock.addTransaction(txn)
                # print(len(newBlock.transactions))
                newBlock.balances=currBalances
                self.txnpool.remove(txn)
                self.verifiedPool.append(txn)                         

        #adding block to blockchain
        newBlock.calculateHash()
        self.blockchain.addBlock(newBlock,prevBlock)
        # print(prevBlock.balances)
        
        # print(newBlock.balances)
        # print(len(newBlock.transactions))
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #broadcasting the block to neighbors
        for neighbor in self.neighbors:
            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,newBlock.size)
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+str(newtimestamp))
           # print(newBlock)
            eventQueue.put([newtimestamp,Event.Event(neighbor,newtimestamp,newBlock,"receiveBlock",ListOfPeers,eventQueue)])
        
        
        
        #adding the event to mine the next block
        nextMine=(np.random.exponential(self.tkMean))
        newtimestamp=timestamp+nextMine
        eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,newBlock,"mineBlock",ListOfPeers,eventQueue)])


    def verifyBlock(self,block,ListOfPeers):
        parentHash=block.previous_hash
        parentBlock=self.blockchain.getBlock(parentHash)
        # for blk in self.blockchain.chain:
        #     if blk.getHash()==parentHash:
        #         parentBlock=blk
        #         break
        
        curBalances=parentBlock.balances.copy()
        for txn in block.transactions:
            if txn.type=="coinbase":
                continue

            senderIdx=-1
            receiverIdx=-1
            for peer in ListOfPeers:
                if peer.getID()==txn.sender:
                    senderIdx=peer.idx
                if peer.getID()==txn.receiver:
                    receiverIdx=peer.idx
            if curBalances[senderIdx]>=txn.amount:
                curBalances[senderIdx]-=txn.amount
                curBalances[receiverIdx]+=txn.amount
            else:
                return False
        return True

    def receiveBlock(self,timestamp,block,ListOfPeers,eventQueue):
        
        parentblock=self.blockchain.getBlock(block.previous_hash)
        
        # 
        if parentblock==None:
            # print("no parent "+self.Id+" "+block.hash)
            # print("no parent "+self.Id+" "+block.owner)   
            self.pending.append(block)
            return

        if not self.verifyBlock(block,ListOfPeers):
            print("verification failed "+self.Id)
            
            self.invalid.append(block)
            return
        #TECHNIQUE1 FOR ENSURING NON REPEATING TRANSACTIONS
        # for txn in block.transactions:
        #     if txn in self.txnpool:
        #         self.txnpool.remove(txn)
        #     if txn not in self.verifiedPool:
        #         self.verifiedPool.append(txn)
    
        #TECHNIQUE2 FOR ENSURING NON REPEATING TRANSACTIONS
        txnpoolCopy=self.txnpool.copy()
        verifiedPoolCopy=self.verifiedPool.copy()
        for txn in block.transactions:
            if txn in verifiedPoolCopy:
                return
            else:
                verifiedPoolCopy.append(txn)
            if txn in txnpoolCopy:
                txnpoolCopy.remove(txn)
        self.txnpool=txnpoolCopy
        self.verifiedPool=verifiedPoolCopy

        self.blockchain.addBlock(block,parentblock)

        #broadcasting the block to neighbors
        for neighbor in self.neighbors:
            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,block.size)
            eventQueue.put([newtimestamp,Event.Event(neighbor,newtimestamp,block,"receiveBlock",ListOfPeers,eventQueue)])  

        #check recursively if children of current block exist in pending
        for blk in self.pending:
            if blk.previous_hash==block.getHash():
                self.pending.remove(blk)
                self.receiveBlock(timestamp,blk,ListOfPeers,eventQueue)

