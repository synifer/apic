import requests
import json
from get_token import get_token
from config import apic

def get_bd():
   token = get_token()

   url = "https://" + str(apic) + "/api/node/class/fvBD.json"
   
   headers = {
      "Cookie" : f"APIC-Cookie={token}", 
   }

   requests.packages.urllib3.disable_warnings()
   response = requests.get(url, headers=headers, verify=False)

   return response

if __name__ == "__main__":
   response = get_bd().json()
   bd = response['imdata']
   
   for item in bd:
      dn = item["fvBD"]['attributes']['dn']
      bd_name = dn.split("/")[-1]
      print(bd_name)
      #print(f"BD name: {item['fvBD']['attributes']['dn']}")
