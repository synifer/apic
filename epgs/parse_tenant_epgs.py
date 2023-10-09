import json
import csv
from pprint import pprint

with open(r'json/tn_epg_v2.json') as f:
    d = json.load(f)
    all_dict = d['imdata']
    epg_list = []
    for i in all_dict:
        epg_name = i['fvAEPg']['attributes']['dn'].split('/')[-1].split("-")[-1]
        epg_list.append(epg_name)
    pprint(epg_list)
    
with open("csv/CARD_PROCESSING_EPG_LIST.csv", mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['EPG NAME'])
    for epg in epg_list:
        writer.writerow([epg])

print("Дані успішно записані у файл CSV.")
    