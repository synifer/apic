import json
import csv
import pandas as pd
from tabulate import tabulate

def extract_data(filename):
    with open(filename) as src:
        data = json.load(src)['imdata']
        
    extracted_data = []

    for item in data:
        if 'fvRsBd' in item:
            bd_name = item['fvRsBd']['attributes']['tnFvBDName']
            app_name = item['fvRsBd']['attributes']['dn'].split("/")[-3].split("-")[-1]
            epg_name = item['fvRsBd']['attributes']['dn'].split("/")[-2].split("-")[-1]
            extracted_data.append([app_name, epg_name, bd_name])
        elif 'fvRsDomAtt' in item:
            domain_name = item['fvRsDomAtt']['attributes']['tDn'].split("/")[-1].split("-")[-1]
            epg = item['fvRsDomAtt']['attributes']['dn'].split("/")[3].split("-")[-1]
            if epg == epg_name:
                extracted_data[-1].append(domain_name)
                
    return extracted_data

def display_table(data):
    headers = ["Application Profile", "Endpint Group", "Bridge Domain", "Domain Name"]
    table = tabulate(data, headers=headers, tablefmt="pretty")
    print(table)

if __name__ == "__main__":
    
    filenames = 'json/apps_dc.json'
    sheet_names = ['DC']
    extracted_data = extract_data(filenames)
    display_table(extracted_data)  
    
    app_data = {sheet: extract_data(filename) for sheet, filename in zip(sheet_names, filenames)}
    dfs = {sheet: pd.DataFrame(list(app_data[sheet].items()), columns=["Application Profile", "Endpint Group", "Bridge Domain", "Domain Name"]) for sheet in sheet_names}
    
    with pd.ExcelWriter('csv/EPGs_FULL_LIST.xlsx', engine='xlsxwriter') as writer:
        for sheet in sheet_names:
            dfs[sheet].to_excel(writer, sheet_name=sheet, index=False)
        
    print("Дані успішно записані у файл EPGs_FULL_LIST.xlsx")

