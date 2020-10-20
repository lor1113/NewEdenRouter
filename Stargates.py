import json
import os

def writer(target,tbw):
    with open(target,'w') as outfile:
        json.dump(tbw,outfile)


def intFilter(strang):
    return int(''.join(c for c in strang if c.isdigit()))

def stargateParse(stargate):
    out = {}
    out["id"] = intFilter(stargate[0])
    out["pair"] = intFilter(stargate[1])
    out["x"] = intFilter(stargate[3])
    out["y"] = intFilter(stargate[4])
    out["z"] = intFilter(stargate[5])
    return out

def systemParse(data,name):
    lineList = [line.rstrip('\n') for line in data]
    out = {}
    out["stargates"] = []
    grabStargate = False
    counter = 0
    stargate = []
    out["name"] = name.split("\\")[2]
    for line in lineList:
        if grabStargate:
            stargate.append(line)
            if "typeID:" in line:
                out["stargates"].append(stargateParse(stargate))
                stargate = []
            if "sunTypeID:" in line:
                grabStargate = False
        if "solarSystemID:" in line:
            out["id"] = intFilter(line)
        if "stargates:" in line:
            grabStargate = True
    return out


def stargateScrape():
    out = {}
    banned = ["UUA-F4", "A821-A", "J7HZ-F", "Pochven"]
    path = "eve/"
    regions = [f.path for f in os.scandir(path) if f.is_dir() and f.name not in banned]
    for region in regions:
        constellations =  [f.path for f in os.scandir(region) if f.is_dir()]
        for constellation in constellations:
            systems = [f.path for f in os.scandir(constellation) if f.is_dir()]
            for system in systems:
                data = open(system + '\\solarsystem.staticdata')
                parsed = systemParse(data,system)
                out[parsed["id"]] = parsed

    return out
writer("stargateDB.json",stargateScrape())