import json
import networkx as nx
import itertools
import math
from networkx import *
AU=149597870700

jsonData = open("stargateDB.json").read()
data = json.loads(jsonData)

baseMap = nx.Graph()


def distAU(sg1, sg2):
    x = (sg1["x"] - sg2["x"]) ** 2
    y = (sg1["y"] - sg2["y"]) ** 2
    z = (sg1["z"] - sg2["z"]) ** 2
    dist = math.sqrt(x + y + z)
    print(dist/AU)
    return dist/AU


def stitch(input, system):
    nodes = [x for x, y in input.nodes(data=True) if y["system"] == system]
    for pair in itertools.combinations(nodes, 2):
        for gate in data[system]["stargates"]:
            if gate["id"] == pair[0]:
                sg1 = gate
            if gate["id"] == pair[1]:
                sg2 = gate
        print(sg1,sg2)
        input.add_edge(pair[0], pair[1], weight=distAU(sg1, sg2), type=1)
    return input


for key, val in data.items():
    for each in val["stargates"]:
        baseMap.add_node(each["id"], system=key)
    baseMap = stitch(baseMap, key)
for key, val in data.items():
    for each in val["stargates"]:
        baseMap.add_edge(each["id"], each["pair"], weight=0, type=0)

write_yaml(baseMap, "baseMap.yaml")
