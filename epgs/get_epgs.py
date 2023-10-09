import requests
import json
from pprint import pprint
#from Authentication.auth import get_token

def get_epg():
   token = get_token()

   url = "https://sandboxapicdc.cisco.com/api/node/class/fvAEPg.json"
   
   headers = {
      "Cookie" : f"APIC-Cookie={token}", 
   }

   requests.packages.urllib3.disable_warnings()
   response = requests.get(url, headers=headers, verify=False)

   return response

if __name__ == "__main__":
   response = get_epg().json()
   epgs = response['imdata']
   

   

   for epg in epgs:
      with open('epg.json', 'w') as f:
         json.dump(epg, f)




   

