
class Event():

    def __init__(self,owner,timestamp,object,eventType,ListOfPeers,eventQueue):
        self.owner=owner
        self.timestamp=timestamp
        self.object=object
        self.eventType=eventType

    def execute(self,ListOfPeers,eventQueue):
    
        if self.eventType=="generateTransaction":
            self.owner.generateTransaction(self.timestamp,ListOfPeers,eventQueue)
        elif self.eventType=="receiveTransaction":
            self.owner.receiveTransaction(self.timestamp,self.object,ListOfPeers,eventQueue)
        else:
            print("Invalid Event Type")

    def __lt__(self, other):
        return self.owner.idx < other.owner.idx
 

