import json
import csv

with open('subnets.json') as src:
    data = json.load(src)
    rows = []

    tenant, bd, subnet, uid = '', '', '', ''

    for item in data.get('imdata', []):
            tenant = item['fvSubnet']['attributes']['dn'].split("/")[1].split("-")[-1]
            bd = item['fvSubnet']['attributes']['dn'].split("/")[2].split("-")[-1]
            subnet = item['fvSubnet']['attributes']['ip']
            uid = item['fvSubnet']['attributes']['uid']
        
              
                          
            rows.append([tenant, bd, subnet, uid])

    with open('subnets.csv', mode='w', newline='') as dst:
        writer = csv.writer(dst)
        writer.writerow(['Tenant', 'Bridge Domain', 'Network', "UID" ])
        for row in rows:
            writer.writerow(row)
