import uuid
import datetime as dt


# Class to store the Node
class Node:
    def __init__(self):
        self.Id = str(uuid.uuid4())
        self.neighbors = []
        self.balance = float(10)
        self.isSlow = False
        self.isLowCPU = False

    def getID(self):
        return self.Id

    def setSlow(self, isSlow):
        self.isSlow = isSlow

    def setLowCPU(self, isLowCPU):
        self.isLowCPU = isLowCPU

    # TODO: SetNeighbors
    # TODO: GetNeighbors
