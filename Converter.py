from networkx import *
import retworkx as rx
import pickle
import json

mapping = {}
map = read_yaml("baseMap.yaml")
retmap = rx.PyGraph()

def writer(target,tbw):
    with open(target,'w') as outfile:
        json.dump(tbw,outfile)

for node in map.nodes(data=True):
    index = retmap.add_node(node)
    mapping[node[0]] = index

for edge in map.edges(data=True):
    retmap.add_edge(mapping[edge[0]],mapping[edge[1]],edge[2])

f = open("retMap", "wb")
pickle.dump(retmap.weighted_edge_list(),f)
f.close()
writer("Mapping.json",mapping)