import json
import csv

with open('json/fabric_nodes.json') as src:
    data = json.load(src)
    rows = []

    node, model, role, serial, id, address, version = '', '', '', '', '', '', ''

    for item in data.get('imdata', []):
        node = item['fabricNode']['attributes']['name']
        model = item['fabricNode']['attributes']['model']
        role = item['fabricNode']['attributes']['role']
        serial = item['fabricNode']['attributes']['serial']
        id = item['fabricNode']['attributes']['id']
        address = item['fabricNode']['attributes']['address']
        version =address = item['fabricNode']['attributes']['version']

       
                            
        rows.append([node, model, role, serial, id, address, version])

    with open('csv/fabric_nodes.csv', mode='w', newline='') as dst:
        writer = csv.writer(dst)
        writer.writerow(['Node', 'Model', 'Role', 'Serial', 'ID', 'Address', "Version"])
        for row in rows:
            writer.writerow(row)
