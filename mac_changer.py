# Importing required modules
import subprocess
import re
import argparse

# Get the current MAC address of a network interface
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


# Change the MAC address of the given interface
def change_mac(interface, new_mac):
     try:
         subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "down"])
         subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac])
         subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "up"])
         print(f"[+] MAC address changed to {new_mac}")
 except Exception as e:
        print(f"[-] Error changing MAC: {e}")

# Command-line argument parser setup
parser = argparse.ArgumentParser(description="MAC Address Changer Tool")
parser.add_argument("-i", "--interface", dest="interface", help="Network interface to change MAC (e.g. eth0)")
parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address (e.g. 00:11:22:33:44:55)")
args = parser.parse_args()


# Check if required arguments are provided
if not args.interface or not args.new_mac:
    parser.print_help()
  exit()

# Show current MAC
current_mac = get_current_mac(args.interface)
print(f"Current MAC: {current_mac}")


# Change MAC
change_mac(args.interface, args.new_mac)

# Verify if MAC changed successfully
new_mac = get_current_mac(args.interface)
if new_mac == args.new_mac:
    print("[+] MAC was successfully changed.")
else:
    print("[-] MAC did not change.")
