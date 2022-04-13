import json

def loadjson(filepath="Things/catalog.json"):
    with open(filepath, 'r', encoding='utf-8') as jsonfile:
        return json.load(jsonfile, encoding='utf-8')

# get_data = loadjson()

def dumpjson(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        return json.dump(data, jsonfile, ensure_ascii=False)


