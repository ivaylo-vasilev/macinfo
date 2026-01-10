#!/usr/bin/env python3

import argparse
import re
import json
import sys
import os

parser = argparse.ArgumentParser(prog="macinfo", description="macinfo - identify device by MAC address", epilog="(c)Ivaylo Vasilev")
parser.add_argument("macaddr", nargs="?", help="specify MAC address")
parser.add_argument("--version", action="version", version="%(prog)s 0.1-beta-3", help="show program version")
args = parser.parse_args()


def main():
    if len(sys.argv) == 1:
        parser.print_help()
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


if __name__ == "__main__":
    main()
