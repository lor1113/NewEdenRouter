import math
import json
import pickle
from retworkx import *

AU = 149597870700
jsonData = open("stargateDB.json").read()
data = json.loads(jsonData)
jsonData = open("Mapping.json").read()
mapping = json.loads(jsonData)
jsonData = open("reverseMapping.json").read()
reverseMapping = json.loads(jsonData)

warpSpeedGL = 0
subSpeedGL = 0
alignGL = 0

def writer(target, tbw):
    with open(target, 'w') as outfile:
        json.dump(tbw, outfile)


def warpTime(warpSpeed, subSpeed, warpDist):
    warpDist = warpDist * AU
    k_accel = warpSpeed
    k_decel = min(warpSpeed / 3, 2)

    warp_dropout_speed = min(subSpeed / 2, 100)
    max_ms_warp_speed = warpSpeed * AU

    accel_dist = AU
    decel_dist = max_ms_warp_speed / k_decel

    minimum_dist = accel_dist + decel_dist

    cruise_time = 0

    if minimum_dist > warpDist:
        max_ms_warp_speed = warpDist * k_accel * k_decel / (k_accel + k_decel)
    else:
        cruise_time = (warpDist - minimum_dist) / max_ms_warp_speed

    accel_time = math.log(max_ms_warp_speed / k_accel) / k_accel
    decel_time = math.log(max_ms_warp_speed / warp_dropout_speed) / k_decel

    total_time = cruise_time + accel_time + decel_time
    return total_time


def mapgen(map):
    with open(map, 'rb') as edges:
        edgeList = pickle.load(edges)
    retMap = PyGraph()
    retMap.extend_from_weighted_edge_list(edgeList)
    for node in retMap.node_indexes():
        retMap[node] = reverseMapping[str(node)]
    return retMap


def edgeWeight(edge):
    if edge["type"] == 0:
        return alignGL
    elif edge["type"] == 1:
        return warpTime(warpSpeedGL,subSpeedGL,edge["weight"])
    elif edge["type"] == 2:
        return edge["weight"]


def routingLength(map, start):
    startID = map.add_node(111)
    edgeData = {"type": 2, "weight": 0}
    for key, val in reverseMapping.items():
        if val == str(start):
            map.add_edge(startID, int(key), edgeData)
    length = graph_dijkstra_shortest_path_lengths(map, startID, edgeWeight)
    map.remove_node(startID)
    return length


def center(map,warp_speed,sub_speed,align_speed):
    map = mapgen(map)
    global alignGL
    global warpSpeedGL
    global subSpeedGL
    alignGL = align_speed
    warpSpeedGL = warp_speed
    subSpeedGL = sub_speed
    out = {}
    counter = 0
    for start in data.keys():
        out[start] = {}
        total = 0
        counter = counter + 1
        if counter % 10 == 0:
            print(counter)
        inter = routingLength(map,start)
        for end,gates in data.items():
            min = 0
            if end != start:
                for gate in gates["stargates"]:
                    gate = gate["id"]
                    val = inter[mapping[str(gate)]]
                    if min == 0:
                        min = val
                    elif val < min:
                        min = val
            total = total + min
        out[start] = total
    return out


writer("center.json",center("retMap",8.69,656,2))
