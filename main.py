import platform
import shutil
import os
import getpass
from datetime import datetime

def system_check():

    print("=" * 45)
    print("       CYBERGUARD SECURITY CHECKER")
    print("=" * 45)

    print("\n[+] SYSTEM INFORMATION")

    print("Hostname:", platform.node())
    print("Operating System:", platform.system())
    print("OS Version:", platform.release())
    print("Architecture:", platform.machine())
    print("Python Version:", platform.python_version())
    print("Current User:", getpass.getuser())

    print("\n[+] DISK SPACE INFORMATION")

    total, used, free = shutil.disk_usage("/")

    print(f"Total Space: {total // (2**30)} GB")
    print(f"Used Space: {used // (2**30)} GB")
    print(f"Free Space: {free // (2**30)} GB")

    print("\n[+] SYSTEM CHECK COMPLETED")

    print("Date:", datetime.now())

    print("=" * 45)


if __name__ == "__main__":
    system_check()
