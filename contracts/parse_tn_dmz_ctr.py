import json 
import csv
from pprint import pprint
from app_and_epg.parse_tn_dmz_epg import epg_list

with open(r'json/contract_v2_747.json') as f:
    data = json.load(f)['imdata']
    
epg_contract_list = []
        
for i in data:
    if 'fvRsProv' in i:
        epg_pr_name = i['fvRsProv']['attributes']['dn'].split("/")[-2].split("-")[-1]
        #epg_pr_ctr_name = i['fvRsCons']['attributes']['dn'].split("/")[-1].split("-")[-1]
        epg_contract_list.append(epg_pr_name)
    elif 'fvRsCons' in i:
        epg_con_name = i['fvRsCons']['attributes']['dn'].split("/")[-2].split("-")[-1]
        #epg_con_ctr_name = i['fvRsCons']['attributes']['dn'].split("/")[-1].split("-")[-1]
        epg_contract_list.append(epg_con_name)
            
        #rows.append([epg_pr_name, epg_con_name])
        
#common_epg = [epg for epg in epg_list if epg in epg_contract_list]
#pprint(f"Unique EPG without contracts: {len(common_epg)}")
common_epg = [epg for epg in epg_list if epg not in epg_contract_list]
unique_epg = list(set(common_epg))

with open("csv/TENANT_DMZ_EGP_WITHOUT_CONTRACT.csv", mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['EPG with Any only Contract'])
    for epg in unique_epg:
        writer.writerow([epg])

print("Дані успішно записані у файл CSV")