import requests
import json
from get_token import get_token
from config import apic

def delete_tenant():
   token = get_token()

   url = "https://" + str(apic) + "/api/mo/uni.json"
   

   payload = {
      "fvTenant": {
         "attributes": {
            "name": "TEST",
            "status": "deleted"
         }
      }
   }

   headers = {
      "Cookie" : f"APIC-Cookie={token}", 
   }

   requests.packages.urllib3.disable_warnings()
   response = requests.post(url,data=json.dumps(payload), headers=headers, verify=False)
   
   if (response.status_code == 200):
      print("Successfully deleted tenant")
   else:
      print("Issue with deleting tenant")

if __name__ == "__main__":
   delete_tenant()
