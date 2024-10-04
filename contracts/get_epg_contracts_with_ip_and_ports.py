import json
import csv
from rich import print

# Initialize an empty list to store rows of data
rows = []

# Initialize variables to store tenant, contract, subject, provider EPG, and consumer EPG
tenant, contract, subject, provider_epg, consumer_epg = '', '', '', '', ''

# Open and load the JSON file containing contract data
with open('json/contracts_dc.json') as src:
    data = json.load(src)
    
    # Iterate over each item in the 'imdata' list
    for item in data.get('imdata', []):
        # Extract tenant name from the distinguished name (dn) attribute
        tenant = item['vzBrCP']['attributes']['dn'].split("/").split("-")[-1]
        # Extract contract name
        contract = item['vzBrCP']['attributes']['name']
        
        # Check if the contract has children (subjects)
        if 'children' in item['vzBrCP']:
            sbj_list = item['vzBrCP']['children']
        
        # Iterate over each subject in the subject list
        for sbj_item in sbj_list:
            if 'vzSubj' in sbj_item:
                subject = sbj_item['vzSubj']['attributes']['name']
                
                # Check if the subject has children (rules)
                if 'children' in sbj_item['vzSubj']:
                    rule_list = sbj_item['vzSubj']['children']
                    
                    # Iterate over each rule in the rule list
                    for rule_item in rule_list:
                        if 'vzRsSubjFiltAtt' in rule_item:
                            rule = rule_item['vzRsSubjFiltAtt']['attributes']
                            ip = rule.get('ip', 'N/A')
                            port = rule.get('port', 'N/A')
                            action = rule.get('action', 'N/A')
                            
                            # Determine provider and consumer EPGs based on contract naming conventions
                            if "_to_" in contract:
                                consumer_epg = contract.split("_to_")
                                provider_epg = contract.split("_to_")[-1].split("_ctr")
                            elif "_L3out_" in contract:
                                provider_epg = contract.split("_ctr") + "_ExtEPG"
                                consumer_epg = 'vzAny'
                            elif "_permit_all_" in contract:
                                provider_epg = 'vzAny'
                                consumer_epg = 'vzAny'
                            
                            # Append the extracted data to the rows list
                            rows.append([tenant, contract, subject, provider_epg, consumer_epg, ip, port, action])

# Write the extracted data to a CSV file
with open('csv/contracts_dc.csv', mode='w', newline='') as dst:
    writer = csv.writer(dst)
    writer.writerow(['Tenant', 'Contract', 'Subject', 'Provider EPG', 'Consumer EPG', 'IP Address', 'Port', 'Action'])
    for row in rows:
        writer.writerow(row)
