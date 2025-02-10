import requests
import json


class CloudflareDNSChecker:
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def list_domains(self):
        url = "https://api.cloudflare.com/client/v4/zones"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            domains = response.json().get("result", [])
            return {domain["name"]: domain["id"] for domain in domains}
        else:
            print(f"Error fetching domains: {response.text}")
            return {}

    def get_dns_records(self, zone_id, record_type=None):
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        params = {}
        if record_type:
            params["type"] = record_type

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(f"Error fetching {record_type} records: {response.text}")
            return []

    def check_mx_records(self, zone_id):
        mx_records = self.get_dns_records(zone_id, "MX")
        if not mx_records:
            print("No MX records found!")
        else:
            print("MX Records:")
            for record in mx_records:
                print(f"  - {record['content']} (Priority: {record['priority']})")

    def check_spf_record(self, zone_id):
        txt_records = self.get_dns_records(zone_id, "TXT")
        spf_records = [record["content"] for record in txt_records if "v=spf1" in record["content"]]

        if not spf_records:
            print("No SPF record found!")
        else:
            print("SPF Record:")
            for spf in spf_records:
                print(f"  - {spf}")

    def check_dkim_record(self, zone_id):
        txt_records = self.get_dns_records(zone_id, "TXT")
        dkim_records = [record["content"] for record in txt_records if "dkim" in record["name"].lower()]

        if not dkim_records:
            print("No DKIM record found!")
        else:
            print("DKIM Records:")
            for dkim in dkim_records:
                print(f"  - {dkim}")


if __name__ == "__main__":
    API_TOKEN = "NON-KEY000-gPCK-Ax2nOaDF"
    checker = CloudflareDNSChecker(API_TOKEN)

    domains = checker.list_domains()
    if domains:
        print("Available Domains:")
        for domain, zone_id in domains.items():
            print(f"  - {domain}: {zone_id}")

        domain_to_check = input("Enter domain name to check: ")
        if domain_to_check in domains:
            ZONE_ID = domains[domain_to_check]
            print("Checking MX, SPF, and DKIM settings...")
            checker.check_mx_records(ZONE_ID)
            checker.check_spf_record(ZONE_ID)
            checker.check_dkim_record(ZONE_ID)
        else:
            print("Domain not found in your Cloudflare account.")
