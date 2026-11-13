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

def port_scan(target):
    print("\n" + "=" * 50)
    print("       CYBERGUARD PORT SCANNER")
    print("=" * 50)

    print(f"\n[+] Target Device: {target}")
    print("[+] Scanning top 20 TCP ports...\n")

    result = subprocess.run(
        ["nmap", "-sV", "--top-ports", "20", target],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[-] Port scan failed!")
        print(result.stderr)
        return

    open_ports = []

    for line in result.stdout.splitlines():
        match = re.search(
            r"^(\d+)/tcp\s+open\s+(\S+)\s*(.*)$",
            line
        )

        if match:
            port = match.group(1)
            service = match.group(2)
            version = match.group(3)

            open_ports.append((port, service, version))

    print("[+] OPEN PORTS DISCOVERED")
    print("-" * 50)

    if open_ports:
        for port, service, version in open_ports:
            print(f"Port: {port}")
            print(f"Service: {service}")
            print(f"Version: {version if version else 'Not identified'}")
            print("-" * 50)
    else:
        print("No open ports discovered.")

    print(f"\n[+] Total open ports: {len(open_ports)}")
    print("[+] Port scan completed.")
    print("=" * 50)


if __name__ == "__main__":
    network_scan("192.168.1.0/24")

    port_scan("192.168.1.74")