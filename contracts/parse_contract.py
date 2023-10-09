import requests
import json
import csv
from datetime import datetime
from pprint import pprint
from parse_tn_cp_epg import epg_list

with open(r'contract.json') as f:
    d = json.load(f)
    
    all_dict = d['imdata']

    tenant_name_list = []
    contract_name_list = []
    provider_epg_name_list = []
    consumer_epg_name_list = []

    for i in all_dict:
        if 'fvRsProv' in i:
            dn_string = i['fvRsProv']['attributes']['dn']
            tenant_name = dn_string.split("/")[1].split("-")[-1]
            contract_name = i['fvRsProv']['attributes']['tnVzBrCPName']
            provider_epg = dn_string.split("/")[-2].split("-")[-1]
            tenant_name_list.append(tenant_name)
            contract_name_list.append(contract_name)
            provider_epg_name_list.append(provider_epg)
        elif 'fvRsCons' in i:
            dn_string = i['fvRsCons']['attributes']['dn']
            tenant_name = dn_string.split("/")[1].split("-")[-1]
            contract_name = i['fvRsCons']['attributes']['tnVzBrCPName']
            consumer_epg = dn_string.split("/")[-2].split("-")[-1]
            tenant_name_list.append(tenant_name)
            contract_name_list.append(contract_name)
            consumer_epg_name_list.append(consumer_epg)


# comparing list epg_list and epg_contract_list
#common_epg = [epg for epg in epg_list if epg in epg_contract_list]
#common_epg = [epg for epg in epg_list if epg not in epg_contract_list]
#unique_epg = list(set(common_epg))
#pprint(f"Unique EPG without contracts: {len(common_epg)}")
#pprint(common_epg)

pprint(contract_name_list)
pprint(tenant_name_list)
pprint(provider_epg_name_list)
pprint(consumer_epg_name_list)
