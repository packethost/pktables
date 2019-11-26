#!/usr/bin/env python3

import argparse
import os
import time

import packet
from netaddr import IPNetwork, IPAddress


PACKETKEY = os.environ.get("PACKET_API_AUTH_TOKEN", os.environ.get("PACKETKEY"))
PROJECTID = os.environ.get("PACKET_PROJECT", os.environ.get("PROJECTID"))
if PACKETKEY is None:
    raise RuntimeError("PACKET_API_AUTH_TOKEN or PACKETKEY(deprecated) env var not set")

if PROJECTID is None:
    raise RuntimeError("PACKET_PROJECT_ID or PROJECTID(deprecated) env var not set")

RULESFILE = os.environ.get("RULESFILE", "/data/pktables.rules")
CHAIN = os.environ.get("CHAIN", "PKTABLES")

manager = packet.Manager(auth_token=PACKETKEY)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update iptables from Packet Production Project."
    )
    parser.add_argument(
        "--dry-run",
        dest="dryrun",
        action="store_true",
        help="do not apply the changes, only display the rules that will be applied",
    )
    args = parser.parse_args()

    networks = []
    data = manager.call_api("projects/%s/ips" % PROJECTID)
    for block in data["ip_addresses"]:
        if not block["management"] and block["address_family"] == 4:
            net = IPNetwork(block["network"] + "/" + str(block["cidr"]))
            networks.append(net)

    alldevs = manager.list_all_devices(PROJECTID)

    devices = {}
    for device in alldevs:
        for ip in device.ip_addresses:
            if ip["address_family"] == 4:
                public = "Public" if ip["public"] else "Private"
                print("checking %s" % ip["address"])
                match = False
                for network in networks:
                    if IPAddress(ip["address"]) in network:
                        print("%s is in network %s" % (ip["address"], network.cidr))
                        match = True
                        break

                if not match:
                    devices[IPAddress(ip["address"])] = {
                        "address": ip["address"],
                        "hostname": device.hostname,
                        "public": public,
                        "address_family": ip["address_family"],
                    }

    if args.dryrun:
        print("<< dry run >>")
        f = "/dev/stdout"
        mode = "a"
    else:
        print("writing rules to %s" % RULESFILE)
        f = RULESFILE
        mode = "w"

    dev_format = """iptables -A {chain} -s {address}  -j ACCEPT -m comment --comment "{hostname} {public} v{address_family}"\n"""  # noqa pylint:disable=line-too-long
    with open(f, mode) as target:
        target.write(
            "# Generated by pktables v1.0.00 on %s\n"
            % time.strftime("%a %b %d %H:%M:%S %Y")
        )
        target.write("iptables -F %s\n" % CHAIN)

        for network in sorted(networks):
            target.write("iptables -A %s -s %s  -j ACCEPT\n" % (CHAIN, network.cidr))

        for ip in sorted(devices):
            target.write(dev_format.format(chain=CHAIN, **devices[ip]))

        target.write("iptables -A %s -j RETURN\n" % CHAIN)
