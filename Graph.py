import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
import Latency
import Transaction
import Event
import Block
import Blockchain
import pydot
from graphviz import Graph

def plotter(ListOfPeers):
    imageFiles=[]
    for peer in ListOfPeers:
        edges=set()
        g=Graph('parent',filename="graph{}.png".format(peer.idx),node_attr={'shape':'box3d','color':'teal'},format="png",edge_attr={'dir':'forward','color':'brown'})
        g.attr(rankdir='LR',splines='line')
        for key in peer.blockchain.chain:
            if key.BlkId == "1":
                g.node(key.BlkId, label="G")
                continue
            g.node(key.BlkId,label=str(key.depth))
        for key in peer.blockchain.chain:
            # peer.blockchain.chain[key]=list(set(peer.blockchain.chain[key]))
            for children in peer.blockchain.chain[key]:
                if (key.BlkId,children.BlkId) in edges:
                    continue
                g.edge(key.BlkId,children.BlkId)
                edges.add((key.BlkId,children.BlkId))

        g.render( 'graphs/'+str(peer.idx),view=False)
        imageFiles.append("graphs/{}.png".format(peer.idx))
    images=[Image.open(x).convert('RGB') for x in imageFiles]  # Open images in binary mode and convert to RGB
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    max_height = sum(heights)
    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    # new_im.save('merged.png')
    images=[Image.open(x).convert('RGB') for x in imageFiles]
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    max_height = sum(heights)+(10*(len(images)+2))
    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (0,x_offset))
        x_offset += im.size[1]
        x_offset += 10
    
    new_im.save('merged.png')


    

