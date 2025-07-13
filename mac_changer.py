import subprocess
import re
import argparse

def get_current_mac(interface):
    try:
        result = subprocess.check_output(["ip", "link", "show", interface], encoding="utf-8")
        mac_address = re.search(r"ether ([\w:]+)", result)
        if mac_address:
            return mac_address.group(1)
        else:
            print("[-] Could not read MAC address.")
