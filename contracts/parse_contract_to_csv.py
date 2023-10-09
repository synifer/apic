import json
import csv
from pprint import pprint
rows = []

tenant, contract, subject, provider_epg, consumer_epg = '', '', '', '', ''
with open('json/contracts_dc.json') as src:
    data = json.load(src)
    for item in data.get('imdata', []):
        tenant = item['vzBrCP']['attributes']['dn'].split("/")[1].split("-")[-1]
        contract = item['vzBrCP']['attributes']['name']
        if 'children' in item['vzBrCP']:
            sbj_list = item['vzBrCP']['children']
        for sbj_item in sbj_list:
            if 'vzSubj' in sbj_item:
                subject = sbj_item['vzSubj']['attributes']['name']

            if "_to_" in contract:
                consumer_epg = contract.split("_to_")[0]
                provider_epg = contract.split("_to_")[-1].split("_ctr")[0]
            elif "_L3out_" in contract:
                provider_epg = contract.split("_ctr")[0] + "_ExtEPG"
                consumer_epg = 'vzAny'
            elif "_permit_all_" in contract:
                provider_epg = 'vzAny'
                consumer_epg = 'vzAny'
            rows.append([tenant, contract, subject, provider_epg, consumer_epg])

with open('csv/contracts_dc.csv', mode='w', newline='') as dst:
    writer = csv.writer(dst)
    writer.writerow(['Tenant', 'Contract', 'Subject', 'Provider EPG', 'Consumer EPG'])
    for row in rows:
        writer.writerow(row)