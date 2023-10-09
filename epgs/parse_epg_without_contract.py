""" 
In parse_tn_dc_epg store Tenant DC EPG list
"""
import json
import csv
import pandas as pd

def parse_epg(filename):
    epg_set = set()  
    with open(filename) as f:
        data = json.load(f)['imdata']    
    for item in data:
        epg_name = item['fvAEPg']['attributes']['dn'].split('/')[-1].split("-")[-1]
        epg_set.add(epg_name)
    
    return epg_set

def parse_epg_ctr(filename):    
    epg_contract_set = set()    
    with open(filename) as f:
        data = json.load(f)['imdata']        
    for i in data:
        if 'fvRsProv' in i:
            epg_pr_name = i['fvRsProv']['attributes']['dn'].split("/")[-2].split("-")[-1]
            epg_contract_set.add(epg_pr_name)
        elif 'fvRsCons' in i:
            epg_con_name = i['fvRsCons']['attributes']['dn'].split("/")[-2].split("-")[-1]
            epg_contract_set.add(epg_con_name)
            
    return epg_contract_set

def write_csv(filename, unique_epg):
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['EPG with Any only Contract'])
        for epg in unique_epg:
            writer.writerow([epg])
        

if __name__ == "__main__":
    
    contract_json_file = 'json/contract_v2_747.json'
    epg_dc_file = 'json/tn_dc_epg_v2.json'
    epg_dmz_file = 'json/tn_dmz_epg_v2.json'
    epg_cp_file = 'json/tn_cp_epg_v2.json'
   
    unique_epg_dc = [epg for epg in parse_epg(epg_dc_file) if epg not in parse_epg_ctr(contract_json_file)]
    unique_epg_dmz = [epg for epg in parse_epg(epg_dmz_file) if epg not in parse_epg_ctr(contract_json_file)]
    unique_epg_cp = [epg for epg in parse_epg(epg_cp_file) if epg not in parse_epg_ctr(contract_json_file)]
      
    #write_csv("csv/TENANT_DC_EPG_WITHOUT_CONTRACT.csv", unique_epg_dc)
    #write_csv("csv/TENANT_DMZ_EPG_WITHOUT_CONTRACT.csv", unique_epg_dmz)
    #write_csv("csv/TENANT_CP_EPG_WITHOUT_CONTRACT.csv", unique_epg_cp)
    
    #  DataFrame для кожного списку EPG
    df_dc = pd.DataFrame({'EPG NAME': unique_epg_dc})
    df_dmz = pd.DataFrame({'EPG NAME': unique_epg_dmz})
    df_cp = pd.DataFrame({'EPG NAME': unique_epg_cp})
    
    # Об'єкт ExcelWriter для запису в один файл з трьома листами
    with pd.ExcelWriter('csv/EPGs_WITHOUT_CONTRACTs.xlsx', engine='xlsxwriter') as writer:
        df_dc.to_excel(writer, sheet_name='DC', index=False)
        df_dmz.to_excel(writer, sheet_name='DMZ', index=False)
        df_cp.to_excel(writer, sheet_name='CP', index=False)
        
    print("Дані успішно записані у файл TENANT_DC_EPG_WITHOUT_CONTRACT.CSV")
