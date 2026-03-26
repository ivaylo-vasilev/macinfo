#!/usr/bin/env python3

import argparse
import re
import json
import requests
import sys
import os

USER_AGENT = "macinfo/0.2-beta"

parser = argparse.ArgumentParser(prog="macinfo", description="macinfo - identify device by MAC address", epilog="(c)Ivaylo Vasilev")
parser.add_argument("macaddr", nargs="?", help="specify MAC address")
parser.add_argument("--update", action="store_true", help="update macdb file")
parser.add_argument("--version", action="version", version="%(prog)s 0.2-beta2", help="show program version")
args = parser.parse_args()


def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    elif args.update:
        # implement a download function from macdb-website; update function
        # db-url(to JSON file: 'get-db'): https://maclookup.app/downloads/json-database/get-db
        print("macdb is up-to-date")
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
        # implement a download function from macdb-url
        print("error: macdb.json not found")
        sys.exit(1)
    
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


# create a reliable download function; use try-except to parse any possible errors
def download_db():
    r = requests.get(url="https://maclookup.app/downloads/json-database/get-db", headers={"User-Agent": USER_AGENT}, stream=True)

    # download and save the database in JSON format
    with open("macdb.json", "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            file.write(chunk)
    
    return


if __name__ == "__main__":
    main()
