""" 
 Script build list with epgs without contract
 and write its to csv file
  
"""

import json
import csv
from pprint import pprint
from app_and_epg.parse_tn_dc_epg import epg_list

with open(r'json/contract_v1_230.json') as f:
    data = json.load(f)['imdata']
    
epg_contract_list = []
        
for i in data:
    if 'fvRsProv' in i:
        epg_pr_name = i['fvRsProv']['attributes']['dn'].split("/")[-2].split("-")[-1]
        #print(f"PROVIDER EPG: {epg_pr_name}")
        epg_contract_list.append(epg_pr_name)
    elif 'fvRsCons' in i:
        epg_con_name = i['fvRsCons']['attributes']['dn'].split("/")[-2].split("-")[-1]
        #print(f"CONSUMER EPG: {epg_con_name}")
        epg_contract_list.append(epg_con_name)

common_epg = [epg for epg in epg_list if epg not in epg_contract_list]
#print(f"COMMON EPG: {common_epg}")
#print(f"UNIQUE EPG: {list(set(common_epg))}")
unique_epg = list(set(common_epg))
#print(unique_epg)
#print(epg_list)

with open("csv/TENANT_DC_EGP_WITHOUT_CONTRACT.csv", mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['EPG with Any only Contract'])
    for epg in unique_epg:
        writer.writerow([epg])

print("Дані успішно записані у файл TENANT_DC_EPG_WITHOUT_CONTRACT.CSV")