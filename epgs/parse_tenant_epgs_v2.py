import json
import csv
from pprint import pprint

def parse_epg(filename):
    epg_set = set() 
    
    with open(filename) as f:
        data = json.load(f)['imdata']
        
    for item in data:
        epg_name = item['fvAEPg']['attributes']['dn'].split('/')[-1].split("-")[-1]
        epg_set.add(epg_name)
    
    return epg_set

if __name__ == "__main__":
    
    json_file = 'json/tn_dc_epg_v2.json'
    csv_file = 'csv/DC_EPG_LIST.csv'
    
    epg_set = parse_epg(json_file)
    
    with open("csv/DC_EPG_LIST.csv", mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['EPG NAME'])
        writer.writerows([[epg] for epg in epg_set])
        
#print(parse_epg(json_file))
print("Дані успішно записані у файл DC_EPG_LIST.CSV")
    
    