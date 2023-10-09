import json
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
    filename = 'json/apps_dc.json'
    extracted_data = extract_data(filename)
    display_table(extracted_data)


with open('json/apps_dc.json') as src:
    data = json.load(src)
    
    rows = []

    app_name, epg_name, bd_name, domain_name = '', '', '', ''

    for item in data.get('imdata', []):
        if 'fvRsBd' in item:
            bd_name = item['fvRsBd']['attributes']['tnFvBDName']
            app_name = item['fvRsBd']['attributes']['dn'].split("/")[-3].split("-")[-1]
            epg_name = item['fvRsBd']['attributes']['dn'].split("/")[-2].split("-")[-1]
        elif 'fvRsDomAtt' in item:
            domain_name = item['fvRsDomAtt']['attributes']['tDn'].split("/")[-1].split("-")[-1]
            epg = item['fvRsDomAtt']['attributes']['dn'].split("/")[3].split("-")[-1]
            domains = []
            if epg == epg_name:
                domains.append(epg)
                
                #rows.append([app_name, epg_name, bd_name, domain_name])
                            
table = tabulate(rows, headers=["Application Profile", "Endpint Group", "Bridge Domain", "Domain Name"], tablefmt="pretty")

print(table)

    #with open('apps_cp.csv', mode='w', newline='') as dst:
    #    writer = csv.writer(dst)
    #    writer.writerow(['Application Profile', 'Endpoint Group', 'Bridge Domain', 'Domain Name'])
    #    for row in rows:
    #        writer.writerow(row)





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

def write_csv(filename, unique_epgs):
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['EPG with Any only Contract'])
        for epg in unique_epgs:
            writer.writerow([epg])

if __name__ == "__main__":
    
    contract_json_file = 'json/contract_v2_747.json'
    epg_dc_file = 'json/tn_dc_epg_v2.json'
    epg_dmz_file = 'json/tn_dmz_epg_v2.json'
    epg_cp_file = 'json/tn_cp_epg_v2.json'
    
    unique_epg_dc = [epg for epg in parse_epg(epg_dc_file) if epg not in parse_epg_ctr(contract_json_file)]
    unique_epg_dmz = [epg for epg in parse_epg(epg_dmz_file) if epg not in parse_epg_ctr(contract_json_file)]
    unique_epg_cp = [epg for epg in parse_epg(epg_cp_file) if epg not in parse_epg_ctr(contract_json_file)]
      
    write_csv("csv/TENANT_DC_EPG_WITHOUT_CONTRACT_DC.csv", unique_epg_dc)
    write_csv("csv/TENANT_DC_EPG_WITHOUT_CONTRACT_DMZ.csv", unique_epg_dmz)
    write_csv("csv/TENANT_DC_EPG_WITHOUT_CONTRACT_CP.csv", unique_epg_cp)
    
    print("Дані успішно записані у файли TENANT_DC_EPG_WITHOUT_CONTRACT.CSV")


import json
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

if __name__ == "__main__":
    
    contract_json_file = 'json/contract_v2_747.json'
    epg_dc_file = 'json/tn_dc_epg_v2.json'
    epg_dmz_file = 'json/tn_dmz_epg_v2.json'
    epg_cp_file = 'json/tn_cp_epg_v2.json'
    
    unique_epg_dc = [epg for epg in parse_epg(epg_dc_file) if epg not in parse_epg_ctr(contract_json_file)]
    unique_epg_dmz = [epg for epg in parse_epg(epg_dmz_file) if epg not in parse_epg_ctr(contract_json_file)]
    unique_epg_cp = [epg for epg in parse_epg(epg_cp_file) if epg not in parse_epg_ctr(contract_json_file)]
    
    # Створіть DataFrame для кожного списку EPG
    df_dc = pd.DataFrame({'EPG with Any only Contract': unique_epg_dc})
    df_dmz = pd.DataFrame({'EPG with Any only Contract': unique_epg_dmz})
    df_cp = pd.DataFrame({'EPG with Any only Contract': unique_epg_cp})
    
    # Створіть об'єкт ExcelWriter для запису в один файл з трьома листами
    with pd.ExcelWriter('csv/TENANT_DC_EPG_WITHOUT_CONTRACT.xlsx', engine='xlsxwriter') as writer:
        df_dc.to_excel(writer, sheet_name='DC', index=False)
        df_dmz.to_excel(writer, sheet_name='DMZ', index=False)
        df_cp.to_excel(writer, sheet_name='CP', index=False)
    
    print("Дані успішно записані у файл TENANT_DC_EPG_WITHOUT_CONTRACT.xlsx")
#======================================================================================


import requests
import csv

# Функція для отримання JSON-даних з ACI
def get_aci_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Помилка при отриманні даних. Код статусу: {response.status_code}")
        return None

# URL до ACI API, який видає дані про EPG
aci_url = "https://{{apic}}/api/node/class/fvAEPg.json?query-target=subtree&rsp-subtree=full&target-subtree-class=fvRsDomAtt,fvRsPathAtt"

# Отримання JSON-даних з ACI
aci_data = get_aci_data(aci_url)

if aci_data is not None:
    epg_list = []

    # Парсинг JSON-даних та виділення EPG без хостів
    for item in aci_data["imdata"]:
        epg_name = item["fvAEPg"]["attributes"]["name"]
        host_attr = item.get("fvAEPg").get("children", [{}])[0].get("fvRsPathAtt", {}).get("attributes", {})
        if not host_attr:
            epg_list.append(epg_name)

    # Запис у CSV-файл
    with open("epg_without_hosts.csv", mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["EPG Name"])
        for epg in epg_list:
            writer.writerow([epg])

    print(f"Записано {len(epg_list)} EPG без хостів у файл epg_without_hosts.csv")
    
    
    import json
import pandas as pd

def parse_epg_without_host(filename):
    epg_data = set()
    with open(filename) as f:
        data = json.load(f)['imdata']        
        for item in data:
            if 'children' not in item['fvAEPg']:
                fvAEP = item['fvAEPg']['attributes']['name']
                epg_data.add(fvAEP)
    return epg_data

if __name__ == "__main__":
    filenames = ['json/dc_epg_details.json', 'json/dmz_epg_details.json', 'json/cp_epg_details.json']
    sheet_names = ['DC', 'DMZ', 'CP']
    
    epg_data = {sheet: parse_epg_without_host(filename) for sheet, filename in zip(sheet_names, filenames)}
    dfs = {sheet: pd.DataFrame({'EPG NAME': epg_data[sheet]}) for sheet in sheet_names}
    
    with pd.ExcelWriter('csv/EPGs_WITHOUT_HOSTS.xlsx', engine='xlsxwriter') as writer:
        for sheet in sheet_names:
            dfs[sheet].to_excel(writer, sheet_name=sheet, index=False)
        
    print("Дані успішно записані у файл EPGs_WITHOUT_HOSTS.xlsx")

#=========================================================================

import json
import csv

# Зчитуємо JSON файл
with open('json/input.json', 'r') as json_file:
    data = json.load(json_file)

# Отримуємо основні дані для запису в CSV
csv_data = []
for item in data['imdata']:
    fvTenant = item['fvTenant']['attributes']
    vzBrCP = item['fvTenant']['children'][0]['vzBrCP']['attributes']
    vzSubj = item['fvTenant']['children'][0]['vzBrCP']['children'][2]['vzSubj']['attributes']
    
    # Формуємо рядок для запису в CSV
    row = [fvTenant['name'], vzBrCP['name'], vzSubj['name']]
    csv_data.append(row)

# Зберігаємо дані у CSV файл
with open('csv/output.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Записуємо заголовки
    csv_writer.writerow(['fvTenant_name', 'vzBrCP_name', 'vzSubj_name'])
    # Записуємо дані
    csv_writer.writerows(csv_data)
    
#========================================================================================================

import json
import csv
from pprint import pprint


# Зчитуємо JSON файл
with open('json/tenant_dmz_subtree.json', 'r') as json_file:
    data = json.load(json_file)

csv_data = []
for item in data['imdata']:
    fvTenant = item['fvTenant']['attributes']['name']
    vzBrCP = item['fvTenant']['children'][0]['vzBrCP']['attributes']['name']
    vzProvDef = item['fvTenant']['children'][0]['vzBrCP']['children'][0]['vzDirAssDef']['children'][0]['vzProvDef']['attributes']['name']
    bdDefDn = item['fvTenant']['children'][0]['vzBrCP']['children'][0]['vzDirAssDef']['children'][0]['vzProvDef']['attributes']['bdDefDn']
    epgDn = item['fvTenant']['children'][0]['vzBrCP']['children'][0]['vzDirAssDef']['children'][0]['vzProvDef']['attributes']['epgDn']
    vzProvDef = item['fvTenant']['children'][0]['vzBrCP']['children'][0]['vzDirAssDef']['children'][0]['vzProvDef']['attributes']['name']
    vzConsDef = item['fvTenant']['children'][0]['vzBrCP']['children'][0]['vzDirAssDef']['children'][1]['vzConsDef']['attributes']['name']
    vzSubj = item['fvTenant']['children'][0]['vzBrCP']['children'][1]['vzSubj']['attributes']['name']
    vzRsSubjFiltAtt_action = item['fvTenant']['children'][0]['vzBrCP']['children'][1]['vzSubj']['children'][0]['vzRsSubjFiltAtt']['attributes']['action']
    vzRsSubjFiltAtt_name = item['fvTenant']['children'][0]['vzBrCP']['children'][1]['vzSubj']['children'][0]['vzRsSubjFiltAtt']['attributes']['tnVzFilterName']
    vzRtProv = item['fvTenant']['children'][0]['vzBrCP']['children'][-2]['vzRtProv']['attributes']['rn'].split("/")[-2].split("-")[-1]
    vzRtCons = item['fvTenant']['children'][0]['vzBrCP']['children'][-1]['vzRtCons']['attributes']['rn'].split("/")[-2].split("-")[-1]
    
    # Формуємо рядок для запису в CSV
    row = [fvTenant, vzBrCP, vzRtProv, vzProvDef, vzRtCons, vzConsDef, vzSubj, vzRsSubjFiltAtt_name]

    csv_data.append(row)

# Зберігаємо дані у CSV файл
with open('csv/output.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Записуємо заголовки
    csv_writer.writerow(['Tenant Name', 'Contract Name', 'Provider APP', 'Provider EPG', 'Consumer APP', 'Consumer EPG', 'Subject', 'Filter'''])
    # Записуємо дані
    csv_writer.writerows(csv_data)


#print(f'Tenant: {fvTenant}')
    #print("\n", "###" * 20, "\n")
    #print(f'Contract: {vzBrCP}')
    #print(f'Provider APP: {vzRtProv}')
    #print(f'Consumer APP: {vzRtCons}')
    #print(f'Provider EPG: {vzProvDef}')
    #print(f'Consumer EPG: {vzConsDef}')
    #print(f'Subject: {vzSubj}')
    #print(f'Filter: {vzRsSubjFiltAtt_name}')
    
    
# ================================================================================================

import json
import csv
from pprint import pprint

with open('json/tenant_dmz_subtree.json', 'r') as src:
    data = json.load(src)

rows = []

for item in data['imdata']:
    fvTenant = item['fvTenant']['attributes']['name']

    for child in item['fvTenant']['children']:
        if 'vzBrCP' in child:
            vzBrCP = child['vzBrCP']['attributes']['name']
            
            
            for vzBrCP_child in child['vzBrCP']['children']:
                if 'vzDirAssDef' in vzBrCP_child:
                    for vzDirAssDef_child in vzBrCP_child['vzDirAssDef']['children']:
                        
                        if 'vzProvDef' in vzDirAssDef_child:
                            vzProvDef = vzDirAssDef_child['vzProvDef']['attributes']['name']
                            ProvApp = vzDirAssDef_child['vzProvDef']['attributes']['epgDn'].split("/")[-2].split("-")[-1]
                                                   
                        if 'vzConsDef' in vzDirAssDef_child:
                            vzConsDef = vzDirAssDef_child['vzConsDef']['attributes']['name']
                            ConsApp = vzDirAssDef_child['vzConsDef']['attributes']['epgDn'].split("/")[-2].split("-")[-1]
                            
                                                   
                elif 'vzSubj' in vzBrCP_child:
                    
                    vzSubj = vzBrCP_child['vzSubj']['attributes']['name']
                
                    
                    for vzSubj_child in vzBrCP_child['vzSubj']['children']:
                        
                        vzRsSubjFiltAtt = vzSubj_child['vzRsSubjFiltAtt']['attributes']['tnVzFilterName']
                        filtr_src = vzSubj_child['vzRsSubjFiltAtt']['attributes']['tDn'].split("/")[1].split("-")[-1]
             

         
                    rows.append([fvTenant, vzBrCP, ProvApp, vzProvDef, ConsApp, vzConsDef, vzSubj, vzRsSubjFiltAtt, filtr_src])
    


with open('csv/output.csv', 'w', newline='') as dst:
    writer = csv.writer(dst)
    writer.writerow(['Tenant Name', 'Contract Name', 'Provider APP', 'Provider EPG', 'Consumer APP', 'Consumer EPG', 'Subject', 'Filter', 'Filter Tenant'])
    for row in rows:    
        writer.writerows(rows)
              
              
# =======================================================================================================================


import json
import csv

with open('json/tenant_dmz_subtree.json', 'r') as src:
    data = json.load(src)

csv_data = []

for item in data['imdata']:
    fvTenant = item['fvTenant']['attributes']['name']

    for child in item['fvTenant']['children']:
        if 'vzBrCP' in child:
            vzBrCP = child['vzBrCP']['attributes']['name']
            
            for vzBrCP_child in child['vzBrCP']['children']:
                if 'vzDirAssDef' in vzBrCP_child:
                    vzDirAssDef = vzBrCP_child['vzDirAssDef']['attributes']['name']
                    
                    for vzSubj_child in vzBrCP_child['vzDirAssDef']['children']:
                        
                        if 'vzProvDef' in vzSubj_child:
                            vzProvDef = vzSubj_child['vzProvDef']['attributes']['name']
                        else:
                            vzProvDef = ""
                            
                        if 'vzConsDef' in vzSubj_child:
                            vzConsDef = vzSubj_child['vzConsDef']['attributes']['name']
                        else:
                            vzConsDef = ""
                        
                        if 'vzSubj' in vzBrCP_child:
                            vzSubj = vzBrCP_child['vzSubj']['attributes']['name']
                        else:
                            vzSubj = ""
                            
                        if 'vzRsSubjFiltAtt' in vzSubj_child:
                            vzRsSubjFiltAtt = vzSubj_child['vzRsSubjFiltAtt']['attributes']['tnVzFilterName']
                        else:
                            vzRsSubjFiltAtt = ""
                            
                        row = [fvTenant, vzBrCP, vzProvDef, vzConsDef, vzSubj, vzRsSubjFiltAtt]
                        csv_data.append(row)

with open('csv/output.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Tenant Name', 'Contract Name', 'Provider EPG', 'Consumer EPG', 'Subject', 'Filter'])
    csv_writer.writerows(csv_data)

# ========================================================================================


import json
import csv

with open('app_profiles_DMZ.json') as src:
    data = json.load(src)
    rows = []

    ap_name, epg_name, bd, domain = '', '', '', ''

    for item in data.get('imdata', []):
        if 'fvAp' in item:
            ap_name = item['fvAp']['attributes']['name']
        elif 'fvAEPg' in item:
            epg_name = item['fvAEPg']['attributes']['name']
        elif 'fvRsBd' in item:
            bd = item['fvRsBd']['attributes']['tnFvBDName']
        elif 'fvRsDomAtt' in item:
            domain = item['fvRsDomAtt']['attributes']['tDn'].split("/")[-1]
            rows.append([ap_name, epg_name, bd, domain])

    with open('app_profiles_DMZ.csv', mode='w', newline='') as dst:
        writer = csv.writer(dst)
        writer.writerow(['Application Profile', 'Endpoint Group', 'Bridge Domain', 'Domain'])
        for row in rows:
            writer.writerow(row)

#=====================================================================================



import json
from collections import defaultdict

def get_apps_details(filename):
    with open(filename) as src:
        data = json.load(src)
    
    app_data = defaultdict(list)

    for item in data.get('imdata', []):
        ap_attributes = item.get('fvAp', {}).get('attributes', {})
        aepg_attributes = item.get('fvAEPg', {}).get('attributes', {})
        rsbd_attributes = item.get('fvRsBd', {}).get('attributes', {})
        rsdomatt_attributes = item.get('fvRsDomAtt', {}).get('attributes', {})
        
        fvAp = ap_attributes.get('name', '')
        fvAEPg = aepg_attributes.get('name', '')
        fvRsBd = rsbd_attributes.get('tnFvBDName', '')
        fvRsDomAtt = rsdomatt_attributes.get('tDn', '').split('/')[-1]

        if any([fvAp, fvAEPg, fvRsBd, fvRsDomAtt]):
            app_data[fvAp].append({
                'fvAEPg': fvAEPg,
                'fvRsBd': fvRsBd,
                'fvRsDomAtt': fvRsDomAtt
            })
    
    return app_data

import json
from collections import defaultdict
from pprint import pprint

with open('json/apps_dc.json') as src:
    data = json.load(src)['imdata']

app_data = defaultdict(lambda: defaultdict(list))

fvAEPg_list = []  # Ініціалізуємо список для fvAEPg поза циклом

for item in data:
    if 'fvAp' in item:
        fvAp = item['fvAp']['attributes']['name']
        # Перевірте, чи вже існує запис для цього fvAp
        if fvAp not in app_data:
            app_data[fvAp] = defaultdict(list)
    elif 'fvAEPg' in item:
        fvAEPg = item['fvAEPg']['attributes']['name']
        fvAEPg_list.append(fvAEPg)
    elif 'fvRsBd' in item:
        fvRsBd = item['fvRsBd']['attributes']['tnFvBDName']
    elif 'fvRsDomAtt' in item:
        fvRsDomAtt = item['fvRsDomAtt']['attributes']['tDn']
        # Додайте дані до поточного fvAp і очистіть список fvAEPg
        app_data[fvAp]['fvAEPg'].extend(fvAEPg_list)
        app_data[fvAp]['fvRsBd'].append(fvRsBd)
        app_data[fvAp]['fvRsDomAtt'].append(fvRsDomAtt)
        fvAEPg_list = []  # Очистіть список для наступних значень fvAEPg

pprint(app_data)


import json
from collections import defaultdict
from pprint import pprint

with open('json/apps_dc.json') as src:
    data = json.load(src)['imdata']

app_data = defaultdict(lambda: defaultdict(list))

for item in data:
    if 'fvAp' in item:
        fvAp = item['fvAp']['attributes']['name']
    elif 'fvAEPg' in item:
        fvAEPg = item['fvAEPg']['attributes']['name']
        fvRsBd = item['fvRsBd']['attributes']['tnFvBDName']
        fvRsDomAtt = item['fvRsDomAtt']['attributes']['tDn'].split('/')[-1]  # Отримати останній шматок URL
        # Додати дані до словника за потрібним порядком
        app_data[fvAp]['fvAEPg'].append(fvAEPg)
        app_data[fvAp]['fvRsBd'].append(fvRsBd)
        app_data[fvAp]['fvRsDomAtt'].append(fvRsDomAtt)

pprint(app_data)

