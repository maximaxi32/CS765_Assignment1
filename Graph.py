import networkx as nx
import matplotlib.pyplot as plt

import Latency
import Transaction
import Event
import Block
import Blockchain

def plotter(ListOfPeers):
    #save_hierarchy_graph_as_png(ListOfPeers[0].blockchain.chain, 'newG.png')
    for i in range(len(ListOfPeers)):
        
        G = nx.Graph(ListOfPeers[i].blockchain.chain)
# Define the adjacency list of block objects

    # Draw the graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=50, font_size=8, font_weight='bold')

    # Save the graph as a PNG file
        plt.savefig("graphs/graph{}.png".format(i))   
        plt.clf()


def save_hierarchy_graph_as_png(graph_dict, filename):
  """Saves a hierarchy graph as a PNG image from a dictionary of key, list pairs.

  Args:
    graph_dict: A dictionary of key, list pairs, where the keys are the nodes in the
      graph and the lists are the children of each node.
    filename: The filename to save the PNG image to.
  """

  # Create a new figure.
  fig = plt.figure()

  # Create a hierarchy graph from the dictionary.
  G = nx.DiGraph()
  for key, children in graph_dict.items():
    G.add_node(key)
    for child in children:
      G.add_edge(key, child)

  # Draw the graph.
  nx.draw(G, with_labels=False,node_size=50, font_size=8, font_weight='bold')

  # Save the figure as a PNG image.
  fig.savefig(filename, format='png')

# Example usage:




