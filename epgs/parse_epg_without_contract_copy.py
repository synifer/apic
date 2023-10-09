import json
import csv
import pandas as pd
from collections import defaultdict
from pprint import pprint

def parse_epg_without_host(filename):    
    
    epg_data = defaultdict(list) 
    with open(filename) as f:
        data = json.load(f)['imdata']        
        for item in data:
            if 'children' not in item['fvAEPg']:
                fvAEP = item['fvAEPg']['attributes']['name']
                fvAPP = item['fvAEPg']['attributes']['dn'].split("/")[-2]
                epg_data[fvAPP].append(fvAEP)
            
                
                
    return epg_data

if __name__ == "__main__":
    
    filenames = ['json/dc_epg_details.json', 'json/dmz_epg_details.json', 'json/cp_epg_details.json']
    sheet_names = ['DC', 'DMZ', 'CP']
    
    epg_data = {sheet: parse_epg_without_host(filename) for sheet, filename in zip(sheet_names, filenames)}
    #dfs = {sheet: pd.DataFrame({'EPG NAME': epg_data[sheet]}) for sheet in sheet_names}
    dfs = {sheet: pd.DataFrame(list(epg_data[sheet].items()), columns=['APP NAME', 'EPG NAME']) for sheet in sheet_names}
    
    with pd.ExcelWriter('csv/EPGs_WITHOUT_HOSTS.xlsx', engine='xlsxwriter') as writer:
        for sheet in sheet_names:
            dfs[sheet].to_excel(writer, sheet_name=sheet, index=False)
        
    print("Дані успішно записані у файл EPGs_WITHOUT_HOSTS.xlsx")
    






#def parse_epg_without_host(filename_json):    
#epg_with_hosts = set()
#epg_without_hosts = defaultdict(list) 
#with open('json/dc_epg_details.json') as f:
#    data = json.load(f)['imdata']        
#    for item in data:
#        if 'children' not in item['fvAEPg']:
#            fvAEP = item['fvAEPg']['attributes']['name']
#            fvAPP = item['fvAEPg']['attributes']['dn'].split("/")[-2]
#            epg_without_hosts[fvAPP].append(fvAEP)
#pprint(epg_without_hosts)


            
            
        
    
    
