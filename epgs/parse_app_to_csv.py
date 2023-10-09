""" 
Script perform two functions. 
First step - function "get_apps_with_epgs(filename)" with
one argument, perform JSON file reading and simple parse methods to find needed object. 
"defaultdict(list)" allow assign item by default for each key in dictionary. Loop "for"
find application profile names, children EPG names and append it to "defaultdict" stored
by "app_data". Function "get_apps_with_epgs" return "app_data"
Second step - function "if __name__ == "__main__"". Here defined list of json files for
function "get_apps_with_epgs(filename)", information for creating sheets in CSV file. 
Comprehense and zip processing json, build csv and write them by "pd.ExcelWriter". pd
mean "pandas"

For get JSON structure used request url  
https://{{apic}}/api/node/class/uni/tn-DMZ/fvAp.json?query-target=subtree

"""

import json
import pandas as pd
from collections import defaultdict
from pprint import pprint

def get_apps_with_epgs(filename):
    
    with open(filename) as src:
        data = json.load(src)['imdata']    
        app_data = defaultdict(list) 

        for item in data:
            if 'fvAp' in item:
                fvAp = item['fvAp']['attributes']['name']
            elif 'fvAEPg' in item:
                fvAEPg = item['fvAEPg']['attributes']['name'].strip()
                app_data[fvAp].append([fvAEPg])
                
    return app_data

#pprint(get_apps_with_epgs('json/apps_dc.json'))
          
if __name__ == "__main__":
    
    filenames = ['json/apps_dc.json', 'json/apps_dmz.json', 'json/apps_cp.json']
    sheet_names = ['DC', 'DMZ', 'CP']    
    
    app_data = {sheet: get_apps_with_epgs(filename) for sheet, filename in zip(sheet_names, filenames)}
    dfs = {sheet: pd.DataFrame(list(app_data[sheet].items()), columns=['APP NAME', 'EPG NAME',]) for sheet in sheet_names}
    
    with pd.ExcelWriter('csv/EPGs_FULL_LIST.xlsx', engine='xlsxwriter') as writer:
        for sheet in sheet_names:
            dfs[sheet].to_excel(writer, sheet_name=sheet, index=False)
        
    print("Дані успішно записані у файл EPGs_FULL_LIST.xlsx")

