# importing libraries
import uuid
import datetime as dt
import numpy as np
import random
import math


class Transaction():    

    def __init__(self,sender,receiver,timestamp,ListOfPeers,type,amount):
        self.ID=str(uuid.uuid4())
        self.sender=sender
        self.receiver=receiver
        self.timestamp=timestamp
        self.type=type
        self.amount=amount

    
    def printTransaction(self,type):
        

        if type=="coinbase":
            
            with open("TxnLog.txt", "a") as myfile:
                myfile.write("TxnID: "+self.ID+" "+str(self.sender)+" mines 50 coins\n")
            return
            
        with open("TxnLog.txt", "a") as myfile:
            myfile.write("TxnID: "+self.ID+" "+str(self.sender)+" pays "+str(self.receiver)+" "+str(self.amount)+" coins\n")
        return

