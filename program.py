import time
from StepParser import *
import yaml
import matplotlib.pyplot as plt
import networkx as nx

start = time.time()
ifc = parse_file('test.step')

print('parsed in ', time.time() - start)

def token_by_id(id):
    for token in ifc:
        if type(token) is not Token:
            continue
        if token.id == id:
            return token
    return None

G = nx.Graph()
labels = {}

def parse_token_to_graph(token, parent = None):
    #print(type(token))
    if type(token) is Anchor:
        tt = token_by_id(token.id)
        if tt is not None:
            labels[parent] = parent
            labels[tt] = tt
            G.add_edge(parent,tt,color='red',weight=1,size=500)
    elif type(token) is Token:
        for a in token.arguments:            
            parse_token_to_graph(a, token)
    elif type(token) is list:
        for item in token:
            parse_token_to_graph(item, parent)    
    else:
        if parent is not None:
            labels[token] = token
            labels[parent] = parent

            G.add_edge(parent,token,color='green',weight=1,size=500)

for token in ifc:
    if type(token) is not Token:
        continue
        
    parse_token_to_graph(token)
            

print(len(G.nodes))
print(len(G.edges))
#pos = nx.kamada_kawai_layout(G)
#nx.draw(G, pos = pos, node_size = 2)

