import json
import csv
from pprint import pprint

#def parse_epg_without_host(filename_json):    
epg_with_fvPathAtt_set = set()
epg_without_fvPathAtt_set = set()      
with open('json/DC_fvAEP_subtree_children.json') as f:
    data = json.load(f)['imdata']        
    for item in data:
        if 'fvAEPg' in item:
            fvAEPg = item['fvAEPg']['attributes']['name']
            aep_children = item['fvAEPg']['children']
            #print(fvAEPg)
            for path in aep_children:
                if 'fvRsPathAtt' in path:
                    host_attr = path['fvRsPathAtt']
                    #fvRsPathAtt = path['fvRsPathAtt']['attributes']
                    epg_with_fvPathAtt_set.add(fvAEPg)
                else:
                    epg_without_fvPathAtt_set.add(fvAEPg)

#pprint(f"як м≥н≥мум один хост в EPG: {epg_with_fvPathAtt_set}"\n)
print("###"*50)
pprint(f"’ост≥в в EPG не ви€влено: {epg_without_fvPathAtt_set}")
           
        
    
    
