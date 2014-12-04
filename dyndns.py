#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import argparse
import pyrax
import pyrax.exceptions as exc
import netifaces

parser = argparse.ArgumentParser()
parser.add_argument('interface')
parser.add_argument('domain')

args = parser.parse_args()

pyrax.set_setting("identity_type", "rackspace")
creds_file = os.path.expanduser("~/.cloud_credentials")
pyrax.set_credential_file(creds_file)
dns = pyrax.cloud_dns

try:
    interface = netifaces.ifaddresses(args.interface)
    interface_ip = interface[netifaces.AF_INET][0]['addr']
except:
    print("Failed to get IP address of interface", args.interface)
    sys.exit()

try:
    dom = dns.find(name=args.domain)
except exc.NotFound:
    print("There is no DNS information for the domain '%s'." % domain_name)
    sys.exit()

try:
    record = dom.find_record("A", name=args.domain)
    print("Current record:", args.domain, "->", record.data)
except:
    print("Error finding apex record")
    sys.exit()

if record.data == interface_ip:
    print("No update required:", record.data, ' == ', interface_ip)
else:
    print("Update required:", record.data, ' != ', interface_ip)
    try:
        record.update(data=interface_ip)
        print("Updating record")
    except:
        print("Error updating record")
        sys.exit()

sys.exit()
