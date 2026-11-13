import subprocess
import shutil
from datetime import datetime


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip(), result.returncode

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "", 1


def check_firewall():
    print("\n[+] FIREWALL SECURITY CHECK")

    if not shutil.which("ufw"):
        print("Firewall: UFW is not installed")
        return

    output, code = run_command(["sudo", "-n", "ufw", "status"])

    if code != 0:
        print("Firewall: Unable to verify (requires permission)")
    elif "Status: active" in output:
        print("Firewall: ACTIVE [PROTECTED]")
    elif "Status: inactive" in output:
        print("Firewall: INACTIVE [WARNING]")
    else:
        print("Firewall: Status unknown")


def check_ssh():
    print("\n[+] SSH SERVICE CHECK")

    if not shutil.which("systemctl"):
        print("SSH: Cannot check service")
        return

    output, code = run_command(["systemctl", "is-active", "ssh"])

    if code == 0 and output == "active":
        print("SSH: RUNNING")
    elif output == "inactive":
        print("SSH: NOT RUNNING")
    else:
        print("SSH: Unknown or service not installed")


def check_automatic_updates():
    print("\n[+] AUTOMATIC SECURITY UPDATES")

    output, code = run_command([
        "dpkg-query", "-W",
        "-f=${Status}", "unattended-upgrades"
    ])

    if code != 0 or "installed" not in output:
        print("Automatic Updates: NOT INSTALLED")
        return

    try:
        with open(
            "/etc/apt/apt.conf.d/20auto-upgrades",
            "r"
        ) as file:
            config = file.read()

        if 'Unattended-Upgrade "1"' in config:
            print("Automatic Updates: ENABLED")
        else:
            print("Automatic Updates: NOT ENABLED")

    except FileNotFoundError:
        print("Automatic Updates: Configuration not found")


def check_root_account():
    print("\n[+] ROOT ACCOUNT SECURITY")

    output, code = run_command([
        "sudo", "-n", "passwd", "-S", "root"
    ])

    if code != 0:
        print("Root Account: Unable to verify")
        return

    parts = output.split()

    if len(parts) >= 2:
        if parts[1] == "L":
            print("Root Account: LOCKED [GOOD]")
        elif parts[1] == "P":
            print("Root Account: PASSWORD SET [REVIEW]")
        elif parts[1] == "NP":
            print("Root Account: NO PASSWORD [WARNING]")


def security_assessment():
    print("=" * 45)
    print("       CYBERGUARD SECURITY ASSESSMENT")
    print("=" * 45)

    check_firewall()
    check_ssh()
    check_automatic_updates()
    check_root_account()

    print("\n" + "=" * 45)
    print("SECURITY ASSESSMENT COMPLETED")
    print("Date:", datetime.now())
    print("=" * 45)


if __name__ == "__main__":
    security_assessment()
