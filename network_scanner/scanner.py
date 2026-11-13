import subprocess
import re
from datetime import datetime

def network_scan(network):
    print("=" * 50)
    print("       CYBERGUARD NETWORK SCANNER")
    print("=" * 50)

    print(f"\n[+] Target Network: {network}")
    print("[+] Starting network discovery...\n")

    result = subprocess.run(
        ["nmap", "-sn", network],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[-] Network scan failed!")
        print(result.stderr)
        return

    # Extract discovered IP addresses
    active_devices = []

    for line in result.stdout.splitlines():
        match = re.search(
            r"^Nmap scan report for (?:.*?\()?(\d{1,3}(?:\.\d{1,3}){3})\)?$",
            line
        )

        if match:
            active_devices.append(match.group(1))

    # Display the scan report
    print("\n[+] NETWORK SCAN RESULTS")
    print("-" * 50)

    if active_devices:
        for number, ip in enumerate(active_devices, start=1):
            print(f"Device {number}: {ip}")
    else:
        print("No active devices discovered.")

    print("-" * 50)
    print(f"[+] Total active devices: {len(active_devices)}")
    print(f"[+] Scan completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\nCYBERGUARD NETWORK SCAN COMPLETED!")
    print("=" * 50)

if __name__ == "__main__":
    network_scan("192.168.1.0/24")    