#!/usr/bin/env python3

import argparse
import re
import json
import requests
import time
import sys
import os

USER_AGENT = "macinfo/0.3.1"

parser = argparse.ArgumentParser(prog="macinfo", description="macinfo - identify device by MAC address", epilog="(c)Ivaylo Vasilev")
parser.add_argument("macaddr", nargs="?", help="specify MAC address")
parser.add_argument("--update", action="store_true", help="update macdb file")
parser.add_argument("--version", action="version", version="%(prog)s 0.3.1", help="show program version")
args = parser.parse_args()


def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    elif args.update:
        # db-url(to JSON file: 'get-db'): https://maclookup.app/downloads/json-database/get-db
        print("[*] updating database...")
        print(download_db(update=True))
        sys.exit(0)
    
    if re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", args.macaddr):
        macaddr = args.macaddr[:8]
    else:
        print(f"error: invalid input for MAC address: {args.macaddr}")
        sys.exit(1)
    
    vendor = mac_address_info(macaddr)
    if vendor == None:
        vendor = "unknown"
    
    print(f"vendor name: {vendor}")
    print(f"mac address: {args.macaddr}")


def mac_address_info(mac):
    if not os.path.exists("macdb.json"):
        print("error: macdb.json not found")
        print("[*] downloading database...")
        print(download_db())
    
    # open and load macdb.json; search for MAC information (vendor)
    with open("macdb.json", "r") as file:
        macdb = json.load(file)
    
    for i in macdb:
        if i["macPrefix"] == mac:
            vendor = i["vendorName"]
            break
        else:
            vendor = None
    
    return vendor


def download_db(update=False):
    try:
        r = requests.get(url="https://maclookup.app/downloads/json-database/get-db", headers={"User-Agent": USER_AGENT}, stream=True)

        # download and save the database in JSON format
        with open("macdb.json", "wb") as file:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)
        
        with open("db-date", "w") as datefile:
            current_date = time.strftime("%Y-%m-%d\n")
            datefile.write(current_date)
        
        if update == True:
            return "[+] database updated"
        else:
            return "[+] database downloaded"
    except requests.exceptions.ConnectionError:
        return "[!] connection error"
    except requests.exceptions.ConnectTimeout:
        return "[!] connection timeout"


if __name__ == "__main__":
    main()
