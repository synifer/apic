import json
import csv
import pandas as pd


def parse_epg_without_host(filename):    
    
    #epg_data = []
    epg_data = {}
    
    with open(filename) as f:
        data = json.load(f)['imdata']        
        for item in data:
            if 'fvAEPg' in item and 'children' not in item['fvAEPg']:
                app_name = item['fvAp']['attributes']['name']
                epg_name = item['fvAEPg']['attributes']['name']
                if app_name not in epg_data:
                    epg_data[app_name] = []
                epg_data[app_name].append(epg_name)
            #if 'children' not in item['fvAEPg']:
             #   fvAEP = item['fvAEPg']['attributes']['name']
              #  epg_data.append(fvAEP)
                                           
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
    





            
            
        
    
    
