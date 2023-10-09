# Links to objects

obj_tenant_fvip = "/api/mo/uni/tn-Heroes.json?query-target=subtree&target-subtree-class=fvIp"
obj_all_fvip = "/api/node/class/fvIp.json"
tenant_tree = "/HarmonyBackupapi/class/fvTenant.json?query-target=subtree"


#Variables

variables:
    {
        url: "https://10.10.20.14",
        username: "user",
        password: "psswd",
        tenant: "Tenant_1",
        vrf: "vrf_1",
        bridge_domains: {
            bd: "Bridge_domain_1",
            gateway: "10.1.1.1",
            mask: "24",
            scope: "shared"
            }
        ap: "Application_1",
        epgs: {
            epg: "Web-epg",
            contract: "web_to_app_bd_contract",
            contract_type: "provider",
            epg: "App-epg",
            contract: "web_to_app_bd_contract",
            contract_type: "consumer",
            epg: "DB-epg"
            contract: "web_to_app_bd_contract",
            contract_type: "consumer"
            }
        contracts: {
            contract: "web_to_app_bd_contract",
            subject: "web_to_app_bd_subject",
            filter: "allow_http",
            }
        filters: {
            filter: "HTTP",
            entry: "http",
            protocol: "tcp",
            port: "80"
            
