import argparse
from Node import *
import random

parser = argparse.ArgumentParser()


def main():
    
    parser.add_argument("--n", type=int)
    parser.add_argument("--z0", type=float)
    parser.add_argument("--z1", type=float)
    args = parser.parse_args()
    n=args.n  
    z0=args.z0
    z1=args.z1
    ListOfPeers=[]
    for _ in range(0,n):
        ListOfPeers.append(Node())
        

#isSlow    
def assign_z0(ListOfPeers,z0,n):         
    numTrues=int((z0*n)/100)
    labels=[True]*numTrues
    labels.append([False]*(n-numTrues))
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setSlow(labels[_])
    

    
#isLow
def assign_z1(ListOfPeers,z1,n):
    numTrues=int((z1*n)/100)
    labels=[True]*numTrues
    labels.append([False]*(n-numTrues))
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setLowCPU(labels[_])    
    
    
    
    


if __name__ == "__main__":
    main()