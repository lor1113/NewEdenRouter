import math
import json
from networkx import *

AU = 149597870700
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
        if edge[2]["type"] == 0:  # 0 is an inter-stargate edge representing align times
            edge[2]["weight"] = align
        if edge[2][
            "type"] == 1:  # 1 is an intra-stargate edge representing warp times, so the warp time is calculated using edge weight
            edge[2]["weight"] = warpTime(warpSpeed, subSpeed, edge[2]["weight"])
    return map


def routingPath(map, start, end):
    map.add_node("Start", system=111)  # adds fake start node
    map.add_node("End", system=999)  # adds fake end node
    for node in map.nodes(data=True):
        if node[1]["system"] == str(start):  # links stargate nodes to start node weight zero
            map.add_edge("Start", node[0])
            print("Start Linked")
        elif node[1]["system"] == str(end):  # links stargate nodes to end node weight zero
            map.add_edge("End", node[0])
            print("End Linked")
    return dijkstra_path(map, "Start", "End")  # calculates shortest path


fenrir_map = read_yaml("Fenrir.yaml")
print(routingPath(fenrir_map, 30000142, 30000144))
