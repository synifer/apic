"""
https://{{apic}}/api/mo/uni/tn-EXAMPLE.json?rsp-subtree=full

"""

import json
import csv
import re
from pprint import pprint

with open('json/tenant_example_subtree.json', 'r') as src:
    data = json.load(src)

rows = []
spl = ".split('/')[-1].split(']')[0].split('-')[1]"

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
                            Provrf = vzDirAssDef_child['vzProvDef']['attributes']['ctxDefDn'].split("/")[-1].strip("]")
                            ProvBD = vzDirAssDef_child['vzProvDef']['attributes']['bdDefDn'].split("-D/")[-1].split("]")[0]
                            ProvApp = vzDirAssDef_child['vzProvDef']['attributes']['epgDn'].split("/")[-2].split("-")[-1]
                                                   
                        if 'vzConsDef' in vzDirAssDef_child:
                            vzConsDef = vzDirAssDef_child['vzConsDef']['attributes']['name']
                            Convrf = vzDirAssDef_child['vzConsDef']['attributes']['ctxDefDn'].split("/")[-1].strip("]")
                            ConsBD = vzDirAssDef_child['vzConsDef']['attributes']['bdDefDn'].split("-D/")[-1].split("]")[0]
                            ConsApp = vzDirAssDef_child['vzConsDef']['attributes']['epgDn'].split("/")[-2].split("-")[-1]

                elif 'vzEpgAnyDef' in vzBrCP_child:
                    for vzEpgAnyDef_child in vzBrCP_child['vzEpgAnyDef']['children']:
                        
                        if 'vzProvDef' in vzEpgAnyDef_child:
                            vzProvDef = vzEpgAnyDef_child['vzProvDef']['attributes']['name']
                            Provrf = vzEpgAnyDef_child['vzProvDef']['attributes']['ctxDefDn'].split("/")[-1].strip("]")
                            ProvBD = vzEpgAnyDef_child['vzProvDef']['attributes']['bdDefDn'].split("-D/")[-1].split("]")[0]
                            ProvApp = vzEpgAnyDef_child['vzProvDef']['attributes']['epgDn'].split("/")[-2].split("-")[-1]
                                                   
                        if 'vzConsDef' in vzEpgAnyDef_child:
                            vzConsDef = vzEpgAnyDef_child['vzConsDef']['attributes']['name']
                            Convrf = vzEpgAnyDef_child['vzConsDef']['attributes']['ctxDefDn'].split("/")[-1].strip("]")
                            ConsBD = vzEpgAnyDef_child['vzConsDef']['attributes']['bdDefDn'].split("-D/")[-1].split("]")[0]
                            ConsApp = vzEpgAnyDef_child['vzConsDef']['attributes']['epgDn'].split("/")[-2].split("-")[-1]
                                  
                elif 'vzSubj' in vzBrCP_child:
                    
                    vzSubj = vzBrCP_child['vzSubj']['attributes']['name']
                
                
                    
                    for vzSubj_child in vzBrCP_child['vzSubj']['children']:
                        
                        vzRsSubjFiltAtt = vzSubj_child['vzRsSubjFiltAtt']['attributes']['tnVzFilterName']
                        filtr_src = vzSubj_child['vzRsSubjFiltAtt']['attributes']['tDn'].split("/")[1].split("-")[-1]
             

         
                        rows.append([fvTenant, vzBrCP, Provrf, ProvBD, ProvApp, vzProvDef, Convrf, ConsBD, ConsApp, vzConsDef, vzSubj, vzRsSubjFiltAtt, filtr_src])
    


with open('csv/tenant_example_contracts.csv', 'w', newline='') as dst:
    writer = csv.writer(dst)
    writer.writerow(['Tenant', 'Contract Name', 'Provider VRF', 'Provider BD', 'Provider APP', 'Provider EPG', 'Consumer VRF', 'Consumer BD','Consumer APP', 'Consumer EPG', 'Subject', 'Filter', 'Filter Tenant'])
    for row in rows:    
        writer.writerows(rows)
              
