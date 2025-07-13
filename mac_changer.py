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
    except subprocess.CalledProcessError:
        print("[-] Error reading interface info.")

def change_mac(interface, new_mac):
     try:
         subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "down"])
         subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac])
         subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "up"])
         print(f"[+] MAC address changed to {new_mac}")
 except Exception as e:
        print(f"[-] Error changing MAC: {e}")

parser = argparse.ArgumentParser(description="MAC Address Changer Tool")
parser.add_argument("-i", "--interface", dest="interface", help="Network interface to change MAC (e.g. eth0)")
parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address (e.g. 00:11:22:33:44:55)")
args = parser.parse_args()
