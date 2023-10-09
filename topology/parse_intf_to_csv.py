import json
import csv
from pprint import pprint
rows = []

node, interface, oper_speed, mtu, layer, admin_status, oper_status, usage, bundle_index, descr, oper_vlans = '','','', '', '', '', '', '', '', '', ''
with open('json/node-122.json') as src:
    data = json.load(src)
    for item in data.get('imdata', []):
        node = item['l1PhysIf']['attributes']['dn'].split("/")[2]
        interface = item['l1PhysIf']['attributes']['id']
        layer = item['l1PhysIf']['attributes']['layer'] 
        admin_status = item['l1PhysIf']['attributes']['adminSt']
        usage = item['l1PhysIf']['attributes']['usage']
        mtu = item['l1PhysIf']['attributes']['mtu']
        #port_channel = item['l1PhysIf']['attributes']['fcotChannelNumber']
        descr = item['l1PhysIf']['attributes']['descr']
        #path_descr = item['l1PhysIf']['attributes']['pathSDescr']
        
        if 'children' in item['l1PhysIf']:
            sbj_list = item['l1PhysIf']['children']
        for sbj_item in sbj_list:
            if 'ethpmPhysIf' in sbj_item:
                oper_speed = sbj_item['ethpmPhysIf']['attributes']['operSpeed']
                oper_status = sbj_item['ethpmPhysIf']['attributes']['operSt']
                bundle_index = sbj_item['ethpmPhysIf']['attributes']['bundleIndex']
                oper_vlans = sbj_item['ethpmPhysIf']['attributes']['operVlans']

         
            rows.append([node, interface, oper_speed, mtu, layer, admin_status, oper_status, usage, bundle_index, descr, oper_vlans])

with open('csv/node-122.csv', mode='w', newline='') as dst:
    writer = csv.writer(dst)
    writer.writerow(['Node', 'Interface', 'Speed', 'MTU', 'Layer', 'Admin status', 'Oper Status', 'Usage', 'Bundle Index', 'Description', 'Oper Vlans'])
    for row in rows:
        writer.writerow(row)