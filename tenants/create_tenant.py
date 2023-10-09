import requests

url = "https://{{apic}}/api/node/mo/uni/tn-N9KWAY1.json"

payload = "{\"fvTenant\":{\"attributes\":{\"dn\":\"uni/tn-N9KWAY1\",\"name\":\"N9KWAY1\",\"rn\":\"tn-N9KWAY1\",\"status\":\"created\"},\"children\":[]}}"
headers = {
  'Content-Type': 'text/plain',
  'Cookie': 'APIC-cookie=eyJhbGciOiJSUzI1NiIsImtpZCI6Im5mejRwMmhuOTQyZXY5YTZjaGF3a2VsMXVvZGI4ZGloIiwidHlwIjoiand0In0.eyJyYmFjIjpbeyJkb21haW4iOiJhbGwiLCJyb2xlc1IiOjAsInJvbGVzVyI6MX1dLCJpc3MiOiJBQ0kgQVBJQyIsInVzZXJuYW1lIjoiYWRtaW4iLCJ1c2VyaWQiOjE1Mzc0LCJ1c2VyZmxhZ3MiOjAsImlhdCI6MTY5MTE0MjIyNiwiZXhwIjoxNjkxMTQyODI2LCJzZXNzaW9uaWQiOiIxeSttRWk2MFRrR3BPSUFVMVNXZU93PT0ifQ.lC0kHmwRETj248WuNu3Q2iIOauPaBd6hBxlw7JNxWSDhCTzU8U7EFntMvprTMky1rrYx12UylTyPxgdI15xsWPInrJxJQVf0BYF2bs7RvaTtHNEz9O9WHdyVpFtU65blP2tLV5UQfDNX-W2xmUPStT12J06MY66JcwTo7l9uc4KsPdAoUXZ1ZpwEGFNTMxg9ELkWp-yglnyL1hRigYojRz_u_Wy5UBrVLmmX-l-9kaA7n2w3TMv0kl1xnc1AR--o93W725c3Q0l0puAAX_vfYrsVOGr2oRo5-vUEaezpnhgHr3k7rXMDcQoCjPpsky9tCxVoy1drT2ix-iPs8iiqSg'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
