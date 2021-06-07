#!/usr/bin/env python3
# Created by Indiana Json github.com/indianajson
# Inspired by Mandatory http://github.com/mandatoryprogrammer/cloudflare_enum
import sys
import json
import requests
import time
import argparse

class cloudfish:
    def __init__(self):
        self.api = "https://api.cloudflare.com/client/v4/zones"
    def records(self,domain,key,email,account,verbose):
        self.domain = domain
        self.key = key
        self.verbose = verbose
        self.email = email
        self.account = account

        if(verbose):
            print("""

 █████╗██╗    █████╗ ██╗  ██╗█████╗  ██████╗██╗██████╗██╗ ██╗
██╔═══╝██║   ██╔══██╗██║  ██║██╔═██╗ ██╔═══╝██║██╔═══╝██║ ██║
██║    ██║   ██║  ██║██║  ██║██║ ██║ ████╗  ██║██████╗██████║
██║    ██║   ██║  ██║██║  ██║██║ ██║ ██╔═╝  ██║╚═══██║██╔═██║
╚█████╗█████╗╚█████╔╝╚█████╔╝█████╔╝ ██║    ██║██████║██║ ██║
 ╚════╝╚════╝ ╚════╝  ╚════╝ ╚════╝  ╚═╝    ╚═╝╚═════╝╚═╝ ╚═╝
          ________________________________________
              FIND SUBDOMAINS USING CLOUDFLARE
                   github.com/indianajson
          ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
            """)

        headers = {
            'X-Auth-Key': key,
            'X-Auth-Email': email,
            'Content-Type': 'application/json',
        }
        create_d = '{"name":"'+domain+'","account":{"id":"'+account+'"},"jump_start":true,"type":"full"}'

        if(verbose):
            print(f"[STATUS] Creating zone for {self.domain} in your {self.email} Cloudflare account.")

        # Sending a request to Cloudflare's API to create the zone.
        create = requests.post(self.api, data=create_d,headers=headers)
        create_r = create.text

        # Error handling for various Cloudflare responses that should kill the script
        if "errors" in create_r and 'code":6103' in create_r:
            print('\033[1;91;40m[ERROR] Wrong credentials. Please check your key and email again.')
            exit(0)
        if "errors" in create_r and 'code":9103' in create_r:
            print('\033[1;91;40m[ERROR] Invalid credentials. Please check your key, email, and account number again.')
            exit(0)
        if "errors" in create_r and 'code":1068' in create_r:
            print('\033[1;91;40m[ERROR] Wrong account number or not enough permissions.')
            exit(0)
        if "errors" in create_r and 'code":1097' in create_r:
            print('\033[1;91;40m[ERROR] The domain you attemped to add is blocked from Cloudflare\'s system.')
            exit(0)
        if "errors" in create_r and 'code":1049' in create_r:
            print('\033[1;91;40m[ERROR] The domain is not registered and cannot be added to Cloudflare.')
            exit(0)
        if "errors" in create_r and 'code":1099' in create_r:
            print('\033[1;91;40m[ERROR] The domain is not real and cannot be added to Cloudflare.')
            exit(0)
        if "errors" in create_r and 'code":1061' in create_r:
            pass
            print(f'\033[1;91;40m[ERROR] A zone for {self.domain} already exists in this account.')
            exit(0)

        create_j = create.json()
        self.zone = create_j["result"]["id"]
        if(verbose):
            print(f"[STATUS] Starting scan of {self.domain} (this will take a moment).")

        scan = requests.post(self.api+'/'+self.zone+'/dns_records/scan',timeout = 60, headers=headers)
        records = requests.get(self.api+'/'+self.zone+'/dns_records?page=1&per_page=100',headers=headers)
        records_j = records.json()


        count = records_j['result_info']['count']
        total_count = records_j['result_info']['total_count']
        page = records_j['result_info']['page']
        total_pages = records_j['result_info']['total_pages']

        #check if any DNS records found
        if count > 0:
            allrecords = []
            if(verbose):
                print(f"[SUCCESS] We found some DNS records for {self.domain}.")
            for record in records_j["result"]:
                if(verbose):
                    print("\t["+record['type']+"] "+record['name']+" ===> "+ record['content'])
                else:
                    allrecords.append(record['type']+"|"+record['name']+"|"+ record['content'])
            #if multiple pages then get the rest of the records
            if page < total_pages:
                i = 1
                while i < total_pages:
                    i=i+1
                    records = requests.get(self.api+'/'+self.zone+'/dns_records?page='+str(i)+'&per_page=100&direction=desc',headers=headers)
                    records_j = records.json()
                    for record in records_j["result"]:
                        if(verbose):
                            print("\t["+record['type']+"] "+record['name']+" ===> "+ record['content'])
                        else:
                            allrecords.append(record['type']+"|"+record['name']+"|"+ record['content'])
        else:
            print('[STATUS] No records found.')
            exit(0)

        if(verbose):
            print(f"[STATUS] Deleting zone for {self.domain}.")

        #delete the zone
        delete = requests.delete(self.api+'/'+self.zone,headers=headers)

        #return the records if not verbose
        if(verbose):
            return ''
        else:
            return allrecords

if __name__ == "__main__":
    # This keeps the program from running if called as a module
    parser = argparse.ArgumentParser(description='Find subdomains with Cloudflare.',usage='%(prog)s -d [domain] -k [globalkey] -e [email on cloudflare] -a [cloudflare account number]')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-k',metavar='ff86g56783...',dest='key',required=True,
                    help='Provide your Cloudflare global key')
    required.add_argument('-d',metavar='example.com',dest='domain',required=True,
                    help='Provide a domain to enumerate (no subdomains)')
    required.add_argument('-e',metavar='john@email.com',dest='email',required=True,
                    help='Provide email on your Cloudflare account')
    required.add_argument('-a',metavar='u3nd92ldhs...',dest='account',required=True,
                    help='Provide your Cloudflare account number')
    optional.add_argument('--verbose',dest='verbose', action='store_true',
                    help='Noisy output with banner and step by step updates')
    args = parser.parse_args()
    try:
        verbose = args.verbose
    except:
        verbose = false

    dns = cloudfish()
    records = dns.records(args.domain,args.key,args.email,args.account,verbose)

    if(not verbose):
        for record in records:
            printable = record.split("|")
            print(printable[0]+"    "+printable[1]+"    "+printable[2])
else:
    pass
