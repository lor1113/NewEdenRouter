import math
import json
import copy
from networkx import *

AU=149597870700
jsonData = open("stargateDB.json").read()
data = json.loads(jsonData)


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

def mapMaker(map, warpSpeed, subSpeed, align):
    for edge in map.edges(data=True):
        if edge[2]["type"] == 0:
            edge[2]["weight"] = align
        if edge[2]["type"] == 1:
            edge[2]["weight"] = warpTime(warpSpeed,subSpeed,edge[2]["weight"])
    return map

def routingPath(map,start,end):
    map.add_node("Start",system=111)
    map.add_node("End",system=999)
    for node in map.nodes(data=True):
        if node[1]["system"] == str(start):
            map.add_edge("Start",node[0])
            print("Start Linked")
        elif node[1]["system"] == str(end):
            map.add_edge("End",node[0])
            print("End Linked")
    print("Modified")
    return dijkstra_path(map,"Start","End")

def routingLength(map,start, end):
    map.add_node("Start",system=111)
    map.add_node("End",system=999)
    for node in map.nodes(data=True):
        if node[1]["system"] == str(start):
            map.add_edge("Start",node[0])
        elif node[1]["system"] == str(end):
            map.add_edge("End",node[0])
    length = dijkstra_path_length(map,"Start","End")
    map.remove_node("Start")
    map.remove_node("End")
    return length

def center(map):
    out = {}
    counter = 0
    for start in data.keys():
        out[start] = 0
        print(start)
        print(out)
        for end in data.keys():
            if end != start:
                counter = counter + 1
                print(counter)
                if counter == 1000:
                    return out
                else:
                    out[start] = out[start] + routingLength(map,start,end)
    return out

read_yaml("Atron.yaml")