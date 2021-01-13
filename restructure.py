import json

with open('dump.json', encoding='utf-8') as fh:
    data = json.load(fh)

new_nodes = []

for node in data['data']['nodes']:
    for stat in data['data']['statsNodes']:

        if node['id'] == stat['node']['id']:
            node["usersTotal"] = stat["usersTotal"] 
            node["usersHalfYear"] = stat["usersHalfYear"]
            node["usersMonthly"] = stat["usersMonthly"] 
            node["localPosts"] = stat["localPosts"] 
            node["localComments"] = stat["localComments"]
            new_nodes.append(node)
            print(node['id'], 'is done.')

new_nodes = json.loads(json.dumps(new_nodes))

with open('restructured_dump.json', 'w', encoding='utf8') as json_file:
    json.dump(new_nodes, json_file, ensure_ascii=False)