# importing libraries
import argparse
import random

# importing other modules
from Node import *
from Network import *

parser = argparse.ArgumentParser()


# This is the main function
# usage: python3 main.py --n N --z0 Z0 --z1 Z1
def main():
    # Parsing user arguments
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--z0", type=float, required=True)
    parser.add_argument("--z1", type=float, required=True)
    args = parser.parse_args()
    n = args.n
    z0 = args.z0
    z1 = args.z1

    # Initializing the list of peer nodes
    ListOfPeers = []
    for _ in range(0, n):
        ListOfPeers.append(Node())
    assign_z0(ListOfPeers, z0, n)
    assign_z1(ListOfPeers, z1, n)
    print("Ok")
    # Creating the network of nodes
    createNetwork(ListOfPeers)


# Funtion to assign isSlow to the Nodes
def assign_z0(ListOfPeers, z0, n):
    numTrues = int((z0 * n) / 100)
    labels = [True] * numTrues
    labelsFalse=[False] * (n - numTrues)
    labels+=labelsFalse
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setSlow(labels[_])


# Funtion to assign isLowCPU to the Nodes
def assign_z1(ListOfPeers, z1, n):
    numTrues = int((z1 * n) / 100)
    labels = [True] * numTrues
    labelsFalse=[False] * (n - numTrues)
    labels+=labelsFalse
    random.shuffle(labels)
    for _ in range(n):
        ListOfPeers[_].setLowCPU(labels[_])


if __name__ == "__main__":
    main()
