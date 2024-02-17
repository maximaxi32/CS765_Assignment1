# importing libraries
import uuid
import datetime as dt
import numpy as np
import random
import math
from dsplot.graph import Graph
import copy
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
        self.minedCnt=0
        self.receivedCnt=0
        
        
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
        currBalances=self.blockchain.getLastBlock().balances
        whatToSend=np.random.uniform(1,currBalances[self.idx]/10)  #ideal case

        if whatToSend<=1:
            with open("TxnLog.txt", "a") as myfile:
                myfile.write("Txn: "+self.Id+" has Insufficient Balance\n")
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
              
        if prevBlock.BlkId != self.blockchain.farthestBlock.BlkId: 
            newprevBlock=self.blockchain.getLastBlock()
            nextMine=(np.random.exponential(self.tkMean))
            newtimestamp=timestamp+nextMine
            eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,newprevBlock,"mineBlock",ListOfPeers,eventQueue)])
            return
        #prevBlock=self.blockchain.getLastBlock()
        if len(self.txnpool)==0:
            #adding the event to mine the next block
            nextMine=(np.random.exponential(self.tkMean))
            newtimestamp=timestamp+nextMine

            eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,prevBlock,"mineBlock",ListOfPeers,eventQueue)])
            return

        self.minedCnt+=1

        newBlock=Block.Block(prevBlock.getHash(),timestamp,self.getID(),prevBlock.depth+1)
       
       
        

        #Adding coinbase transaction
        coinbasetxn=Transaction.Transaction(self.getID(),self.getID(),timestamp,ListOfPeers,"coinbase",50)
        newBlock.addTransaction(coinbasetxn)
        coinbasetxn.printTransaction("coinbase")

       
        currBalances=listCopier(prevBlock.balances)   #create a balance copy
        newBlock.balances=currBalances    #Added this to prevent balances from going NULL
        for txn in self.txnpool:
            if newBlock.size>=990:
                break
            senderIdx=-1
            receiverIdx=-1
            # To get the indices of sender and receiver
            for peer in ListOfPeers:
                if peer.getID()==txn.sender:
                    senderIdx=peer.idx
                if peer.getID()==txn.receiver:
                    receiverIdx=peer.idx

            
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
        # print(self.blockchain.farthestBlock.BlkId, self.blockchain.farthestBlock.depth) 
        self.blockchain.addBlock(newBlock,self.blockchain.farthestBlock)
        if newBlock.depth>self.blockchain.longestLength:
            self.blockchain.longestLength = newBlock.depth
            self.blockchain.farthestBlock=newBlock

        # if self.idx==0:
        #     for blk in self.blockchain.chain.keys():
        #         print(blk,self.blockchain.chain[blk])
        # print(prevBlock.balances)
        
        # print(newBlock.balances)
        # print(len(newBlock.transactions))
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #broadcasting the block to neighbors
        for neighbor in self.neighbors:
            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,newBlock.size)
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+str(newtimestamp))
           # print(newBlock)
            newDeepBlock=newBlock.deepCopyBlk()          
            eventQueue.put([newtimestamp,Event.Event(neighbor,newtimestamp,newDeepBlock,"receiveBlock",ListOfPeers,eventQueue)])
        
        
        
        #adding the event to mine the next block
        nextMine=(np.random.exponential(self.tkMean))
        newtimestamp=timestamp+nextMine
        eventQueue.put([newtimestamp,Event.Event(self,newtimestamp,newBlock,"mineBlock",ListOfPeers,eventQueue)])


    def verifyBlock(self,block,ListOfPeers):
        parentHash=block.previous_hash
        parentBlock=self.blockchain.getBlock(parentHash)
        
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

        
        for blk in self.blockchain.chain:
            if blk.BlkId==block.BlkId:
                return
        parentblock=self.blockchain.getBlock(block.previous_hash)
        


        if parentblock==None:
            if block in self.pending:
                return
            self.pending.append(block)
      
            return
        copyOfBlk=block.deepCopyBlk()

        if not self.verifyBlock(copyOfBlk,ListOfPeers):
            print("verification failed "+self.Id)
            
            self.invalid.append(copyOfBlk)
            return



    
        #TECHNIQUE2 FOR ENSURING NON REPEATING TRANSACTIONS
        txnpoolCopy=listCopier(self.txnpool)
        verifiedPoolCopy=listCopier(self.verifiedPool)
        for txn in copyOfBlk.transactions:
            if txn in verifiedPoolCopy:
               pass
            else:
                verifiedPoolCopy.append(txn)
            if txn in txnpoolCopy:
                txnpoolCopy.remove(txn)
        self.txnpool=txnpoolCopy
        self.verifiedPool=verifiedPoolCopy

        self.receivedCnt+=1
        copyOfBlk.depth=parentblock.depth+1
        if copyOfBlk.depth>self.blockchain.longestLength:   
            self.blockchain.longestLength=copyOfBlk.depth
            self.blockchain.farthestBlock=copyOfBlk

        self.blockchain.addBlock(copyOfBlk,parentblock)

        #check recursively if children of current block exist in pending
        before=0
        if self.idx==0:
            before=len(self.pending)
       
        stillsearching=True
        while stillsearching==True and len(self.pending)>0:
            stillsearching=False
            for blk in self.pending:
                
                for currBlock in self.blockchain.chain:

                    if blk.previous_hash==currBlock.getHash():
                        self.pending.remove(blk)
                        #print(block.depth)
                        self.blockchain.addBlock(blk,currBlock)
                        blk.depth=currBlock.depth+1
                        if blk.depth>self.blockchain.longestLength:
                            self.blockchain.longestLength=blk.depth
                            self.blockchain.farthestBlock=blk
                        
                        for neighbor in self.neighbors:
                            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,blk.size)
                            eventQueue.put([newtimestamp,Event.Event(neighbor,newtimestamp,blk.deepCopyBlk(),"receiveBlock",ListOfPeers,eventQueue)])  
                        stillsearching=True
                        break
            
                    # self.receiveBlock(timestamp,blk,ListOfPeers,eventQueue)
        
        
        
        
        #broadcasting the block to neighbors
        for neighbor in self.neighbors:
            newtimestamp=timestamp+Latency.generateLatency(ListOfPeers,self.idx,neighbor.idx,copyOfBlk.size)
            eventQueue.put([newtimestamp,Event.Event(neighbor,newtimestamp,copyOfBlk,"receiveBlock",ListOfPeers,eventQueue)])  


def listCopier(lst):
    copylst=[]
    for i in lst:
        copylst.append(i)
    return copylst


