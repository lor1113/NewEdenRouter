import json

jsonData = open("stargateDB.json").read()
data = json.loads(jsonData)
jsonData = open("stargateLocation.json").read()
locations = json.loads(jsonData)

def writer(target,tbw):
    with open(target,'w') as outfile:
        json.dump(tbw,outfile)


for key,val in data.items():
    for stargate in val["stargates"]:
        stargate["destination"] = locations[str(stargate["pair"])]

writer("stargateDB.json",data)