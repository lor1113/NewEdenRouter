import math
import json
import pickle
from retworkx import *

AU = 149597870700  # Astronomical Unit in meters
jsonData = open("stargateDB.json").read()  # used for system and stargate data
data = json.loads(jsonData)
jsonData = open("Mapping.json").read()  # used to map stargate IDs to internal node IDs
mapping = json.loads(jsonData)
jsonData = open("reverseMapping.json").read()  # the mapping of node IDs to the system their stargate is in
reverseMapping = json.loads(jsonData)

warpSpeedGL = 0  # Global variables for Warp Speed, Sublight Speed, and Align time.
subSpeedGL = 0  # Used to feed the EdgeWeight function
alignGL = 0  # Unfortunately required as the function is automatically used by the package and can only have one input


def writer(target, tbw):  # basic utility function to write Json
    with open(target, 'w') as outfile:
        json.dump(tbw, outfile)


def warpTime(warpSpeed, subSpeed, warpDist):  # Calculates warp time
    warpDist = warpDist * AU  # Calculates warp distance in m by multiplying input in AU by constant of m in AU
    k_accel = warpSpeed
    k_decel = min(warpSpeed / 3, 2)  # warp deceleration is usually half of the warp speed but is also capped at 3AU/s^2

    warp_dropout_speed = min(subSpeed / 2, 100)  # Likewise warp dropout speed is half of sublight speed or capped at 100m/s
    max_ms_warp_speed = warpSpeed * AU  # maximum warp speed in m/s, calculated bu multiplying by constant of m in AU

    accel_dist = AU  # The way warp acceleration works in EVE is that one always travels exactly one AU while accelerating from 0 to max warp speed
    decel_dist = max_ms_warp_speed / k_decel  # how long distance wise will be spent decelerating

    minimum_dist = accel_dist + decel_dist  # the minimum warp distance for there to be a period of travel at maximum speed instead of beginning to
    # decelerate before reaching it

    cruise_time = 0

    if minimum_dist > warpDist:  # if there will not be a period of maximum speed travel,
        max_ms_warp_speed = warpDist * k_accel * k_decel / (k_accel + k_decel)  # top speed reached in warp if not maximum
    else:
        cruise_time = (warpDist - minimum_dist) / max_ms_warp_speed  # if there will be a period of maximum speed travel how long will it take

    accel_time = math.log(max_ms_warp_speed / k_accel) / k_accel  # how long to accelerate to top speed reached during warp, which is not
    # necessarily maximum warp speed
    decel_time = math.log(max_ms_warp_speed / warp_dropout_speed) / k_decel  # how long to decelerate from top speed reached in warp to warp
    # dropout speed

    total_time = cruise_time + accel_time + decel_time
    return total_time


def mapgen(map):  # Map loader. Depickles a weighted edge list and builds a graph from it
    with open(map, 'rb') as edges:
        edgeList = pickle.load(edges)
    retMap = PyGraph()
    retMap.extend_from_weighted_edge_list(edgeList)
    for node in retMap.node_indexes():  # adds stargate IDs to the nodes as data using a precompiled JSON list
        retMap[node] = reverseMapping[str(node)]
    return retMap


def edgeWeight(edge):
    if edge["type"] == 0:  # 0 is an inter-stargate edge representing align times
        return alignGL
    elif edge["type"] == 1:  # 1 is an intra-stargate edge representing warp times, so the warp time is calculated using edge weight
        return warpTime(warpSpeedGL, subSpeedGL, edge["weight"])
    elif edge["type"] == 2:  # 2 is a special edge used to connect "system" start nodes to system stargates; it is always 0
        return edge["weight"]


def routingLength(map, start):
    startID = map.add_node(111)  # creates a node used to simulate starting in a system; because starting at any one stargate would be undue bias
    edgeData = {"type": 2, "weight": 0}
    for key, val in reverseMapping.items():  # cycles through all stargate nodes linking those that belong to the start system to it
        if val == str(start):
            map.add_edge(startID, int(key), edgeData)
    length = graph_dijkstra_shortest_path_lengths(map, startID, edgeWeight)  # Inbuilt function which calculates all shortest paths from a node
    map.remove_node(startID)  # removes temporary system node
    return length


def center(map, warp_speed, sub_speed, align_speed):
    map = mapgen(map)  # loads map
    global alignGL  # calling global scope
    global warpSpeedGL
    global subSpeedGL
    alignGL = align_speed  # setting globals
    warpSpeedGL = warp_speed
    subSpeedGL = sub_speed
    out = {}
    counter = 0
    for start in data.keys():  # iterates through all systems
        out[start] = {}
        total = 0
        counter = counter + 1
        if counter % 10 == 0:  # simple counter to visualize progress
            print(counter)
        inter = routingLength(map, start)  # gets shortest paths for current system
        for end, gates in data.items(): # Since nodes in this map are stargates not systems, they need to be compacted down into system-system
            # distances instead of system-stargate distances, this is done by iterating through the results and using only the shortest distance
            # for each system as the system-system length
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


writer("center.json", center("retMap", 8.69, 656, 2))
