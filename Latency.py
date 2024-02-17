# importing libraries
import uuid
import datetime as dt
import numpy as np
import random
import math
from collections import defaultdict
# importing other modules
import Node
import Network

#enter msgSize in KBs
def generateLatency(ListOfPeers,i,j,msgSize):
    
    c=0
    if (not ListOfPeers[i].getSlow()) and (not ListOfPeers[j].getSlow()):
        c=100
    else :
        c=5
    #everything is in units of bits and seconds
    d=np.random.exponential(96*1000/(c*1000000))
    rho=ListOfPeers[i].rhos[j]
    latency=10*((rho)+(msgSize*1000*8/(c*1000000))+d)
    return latency

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

# def main():
#     ListOfPeers=[]
#     for _ in range(0, 5):
#         ListOfPeers.append(Node.Node(5))
#     rhoMatrix=nested_dict(5, float)
#     for i in range(5):
#         for j in range(i):
#             currentRho=np.random.uniform(0.01,0.5)
#             rhoMatrix[ListOfPeers[i].getID()][ListOfPeers[j].getID()]=currentRho
#             rhoMatrix[ListOfPeers[j].getID()][ListOfPeers[i].getID()]=currentRho
            
#     for i in range(5):
#         for j in range(5):
#             if i==j:
#                 continue
#             print((rhoMatrix[ListOfPeers[i].getID()][ListOfPeers[j].getID()]),end=" ")
#             #print(generateLatency(ListOfPeers,i,j,rhoMatrix[ListOfPeers[i].getID()][ListOfPeers[j].getID()]),end=" ")
#         print("")

    
# if __name__=="__main__":
#     main()
            
    
    