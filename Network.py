# To create a network of Peer Nodes
def createNetwork(ListofPeers):
    pass

# To check if the network is a connected graph or not


def isConnected(ListOfPeers):
    if not ListOfPeers:
        return True
    visited = set()
    start_node = ListOfPeers[0]
    dfs(start_node, visited)
    return len(visited) == len(ListOfPeers)

def dfs(node, visited):
    visited.add(node)
    currNeighbors = node.GetNeighbors()
    for neighbor in currNeighbors:
        if neighbor not in visited:
            dfs(neighbor, visited)

