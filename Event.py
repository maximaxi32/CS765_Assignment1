# class describing an event from the event queue
class Event:
    # constructor
    def __init__(self, owner, timestamp, object, eventType, ListOfPeers, eventQueue):
        self.owner = owner
        self.timestamp = timestamp
        self.object = object
        self.eventType = eventType

    # function to execute the event, depending on the event type
    def execute(self, ListOfPeers, eventQueue):
        if self.eventType == "generateTransaction":
            self.owner.generateTransaction(self.timestamp, ListOfPeers, eventQueue)
        elif self.eventType == "receiveTransaction":
            self.owner.receiveTransaction(
                self.timestamp, self.object, ListOfPeers, eventQueue
            )
        elif self.eventType == "mineBlock":
            self.owner.mineBlock(self.timestamp, self.object, ListOfPeers, eventQueue)
        elif self.eventType == "receiveBlock":
            self.owner.receiveBlock(
                self.timestamp, self.object.deepCopyBlk(), ListOfPeers, eventQueue
            )
        else:
            print("Invalid Event Type")

    # custom comparator for comparing to events having equal timestamps
    def __lt__(self, other):
        return self.owner.idx < other.owner.idx
