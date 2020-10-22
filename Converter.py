import networkx as nx
from networkx import *
import retworkx as rx#
import json

mapping = {}
reverseMapping = {}
map = read_yaml("baseMap.yaml")
retmap = rx.PyGraph()

def writer(target,tbw):
    with open(target,'w') as outfile:
        json.dump(tbw,outfile)

for node in map.nodes(data=True):
    index = retmap.add_node(node)
    mapping[node[0]] = index
    reverseMapping[index] = node[0]

for edge in map.edges(data=True):
    retmap.add_edge(mapping[edge[0]],mapping[edge[1]],edge[2])

writer("retMap.json",retmap.weighted_edge_list())
writer("Mapping.json",mapping)
writer("reverseMapping.json",reverseMapping)