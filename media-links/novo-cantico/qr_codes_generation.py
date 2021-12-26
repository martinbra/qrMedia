import json


with open('novo-cantico.json', 'r') as fp:
    nc = json.load(fp)

nc = [(int(i), url) for i, url in nc.items()]



