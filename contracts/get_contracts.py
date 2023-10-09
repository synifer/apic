import requests
import json
from pprint import pprint
#from Authentication.auth import get_token

def get_contract():
   token = get_token()

   url = "https://{{apic}}}/api/node/class/fvAEPg.json?query-target=children&target-subtree-class=fvRsCons,fvRsProv"
   
   headers = {
      "Cookie" : f"APIC-Cookie={token}", 
   }

   requests.packages.urllib3.disable_warnings()
   response = requests.get(url, headers=headers, verify=False)

   return response

if __name__ == "__main__":
   response = get_contract().json()
   contracts = response['imdata']
   
   contract_list = []

   
   for contract in contracts:
      
      with open('contract.json', 'w') as f:
         json.dump(contract, f)

