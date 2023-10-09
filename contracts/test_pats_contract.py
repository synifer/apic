import json
import csv

# Зчитування даних з файлу JSON
with open('json/contract.json') as f:
    data = json.load(f)['imdata']

epg_contract_list = []

# Перевірка кожного об'єкта в JSON
for item in data:
    if 'fvRsProv' in item:
        pr_dn = item['fvRsProv']['attributes']['dn']
        epg_pr_name = pr_dn.split("/")[-2]
        epg_contract_list.append(epg_pr_name)
    elif 'fvRsCons' in item:
        con_dn = item['fvRsCons']['attributes']['dn']
        epg_con_name = con_dn.split("/")[-2]
        epg_contract_list.append(epg_con_name)

# Знайдення унікальних EPG, які не мають контрактів
epg_list = ["EPG1", "EPG2", "EPG3"]  # Ваш список EPG, яким потрібні контракти
unique_epg = list(set(epg_list) - set(epg_contract_list))

# Запис у файл CSV
with open("csv/epg_only_with_any_contract.csv", mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['EPG with Any only Contract'])
    for epg in unique_epg:
        writer.writerow([epg])

print("Дані успішно записані у файл CSV.")

import json
import csv
from app_and_epg.parse_tn_dc_epg import epg_list

with open(r'json/contract_v1_230.json') as f:
    data = json.load(f)['imdata']

epg_contract_set = set()  # Використовуємо множину для ефективного пошуку
unique_epg = set(epg_list)

for item in data:
    if 'fvRsProv' in item:
        epg_pr_name = item['fvRsProv']['attributes']['dn'].split("/")[-2].split("-")[-1]
        epg_contract_set.add(epg_pr_name)
    elif 'fvRsCons' in item:
        epg_con_name = item['fvRsCons']['attributes']['dn'].split("/")[-2].split("-")[-1]
        epg_contract_set.add(epg_con_name)

# Знаходимо унікальні EPG, які відсутні в epg_contract_set
unique_epg_without_contract = unique_epg - epg_contract_set

with open("csv/TENANT_DC_EPG_WITHOUT_CONTRACT.csv", mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['EPG with Any only Contract'])
    for epg in unique_epg_without_contract:
        writer.writerow([epg])

print("Дані успішно записані у файл TENANT_DC_EPG_WITHOUT_CONTRACT.CSV")

