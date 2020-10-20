import json

jsonData = open("stargateDB.json").read()
data = json.loads(jsonData)
stargates = {}

def writer(target,tbw):
    with open(target,'w') as outfile:
        json.dump(tbw,outfile)

for key,val in data.items():
    for stargate in val["stargates"]:
        stargates[stargate["id"]] = key

writer("stargateLocation.json",stargates)