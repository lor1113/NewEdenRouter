import json
jsonData = open("center.json").read()
center = json.loads(jsonData)
jsonData = open("stargateDB.json").read()
systems = json.loads(jsonData)

min = 0
closest = 0
for system,value in center.items():
    if min == 0:
        min = value
        closest = system
    elif min > value:
        min = value
        closest = system
print(closest)
print(min)
