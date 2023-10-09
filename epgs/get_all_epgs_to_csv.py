import requests
import json
import csv
from datetime import datetime
from get_token import get_token
from config import apic
from obj import obj_all_fvip


csv_filename = 'epgs_ips_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'

def get_ipaddr():
   token = get_token()

   url = "https://" + str(apic) + str(obj_all_fvip)
   
   headers = {
      "Cookie" : f"APIC-Cookie={token}", 
   }

   requests.packages.urllib3.disable_warnings()
   response = requests.get(url, headers=headers, verify=False)
   
   return response

if __name__ == "__main__":
   response = get_ipaddr().json()
   epg_info = response['imdata']

   with open(csv_filename, mode="w", newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['Tenant Name', 'VRF Name', 'AP Name', 'EPG Name', 'BD Name', 'IP address', "MAC address", "Node ID"])
      #writer.writerow(['Tenant Name', 'VRF Name', 'AP Name' 'EPG Name', 'BD Name' 'IP address', 'MAC address', 'Node ID', 'Ports'])

      for item in epg_info:
         tenant_name = item['fvIp']['attributes']['vrfDn'].split("/")[-2]
         vrf_name = item['fvIp']['attributes']['vrfDn'].split("/")[-1]
         ap_name = item['fvIp']['attributes']['dn'].split("/")[-4]
         epg_name = item['fvIp']['attributes']['dn'].split("/")[-3]
         #epg_name = item['fvIp']['attributes']['dn'].split('/epg-')[1].split('_epg')[0]
         bd_name = item['fvIp']['attributes']['bdDn'].split("/")[-1]
         ip_addr = item['fvIp']['attributes']['addr']
         mac_addr = item['fvIp']['attributes']['dn'].split("/")[-2].split("-")[-1]
         #node_id = item['fvIp']['attributes']['fabricPathDn'].split("/")[1]
         node_id = item['fvIp']['attributes']['fabricPathDn'].split("/")[2].split("-")[-1]
         #port_path = item['fvIp']['attributes']['fabricPathDn'].split("/")[-1].split("-")[-1].split("_")
         #intpolgr = port_path
         #ports = []
         #for item in intpolgr:
         #  if item.isdigit() and (int(item) == 45 or int(item) == 46):
         #     ports.append(item)
         #port_path = item['fvIp']['attributes']['fabricPathDn'].split("/")[-1]
         #writer.writerow([tenant_name, vrf_name, ap_name, epg_name, bd_name, ip_addr, mac_addr, node_id, port_path])
         writer.writerow([tenant_name, vrf_name, ap_name, epg_name, bd_name, ip_addr, mac_addr, node_id])
      print(f"Data saved to file {csv_filename}")
   
  
