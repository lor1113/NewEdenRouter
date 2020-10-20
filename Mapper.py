import math
import json
import networkx as nx
from statistics import mean
from networkx import *
import operator
map = read_yaml("newKspace.yaml")
AU=149597870700

def getDistance(dist):
    if dist > 1e9:
        return (dist / AU, "AU")
    else:
        return (dist/1000, "KM")

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

nodeList = list(nodes(map))
print(len(nodeList))