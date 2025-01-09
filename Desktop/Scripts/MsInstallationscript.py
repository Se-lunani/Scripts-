import os
import subprocess
import time

# List of IP addresses or hostnames of the 50 computers
computers = [
    "computer1.local",
    "computer2.local",
    # Add the rest of the computers' IP addresses or hostnames here
]

# Microsoft Office installer URL (replace with the actual download URL)
office_installer_url = "https://aka.ms/OfficeSetup"

# Remote PowerShell script to run the installer
powershell_script = f"""
$ErrorActionPreference = "Stop"

# Download Office Installer
Invoke-WebRequest -Uri "{office_installer_url}" -OutFile "C:\\Users\\Public\\Downloads\\OfficeSetup.exe"

# Start the installation process
Start-Process -FilePath "C:\\Users\\Public\\Downloads\\OfficeSetup.exe" -ArgumentList "/quiet" -Wait

# Wait for installation to complete
Start-Sleep -Seconds 1800  # Adjust time depending on installation size and network speed

# Cleanup installer
Remove-Item "C:\\Users\\Public\\Downloads\\OfficeSetup.exe"
"""

def run_remote_installation(computer):
    try:
        # Execute PowerShell command remotely
        command = f"powershell.exe -Command Invoke-Command -ComputerName {computer} -ScriptBlock {{ {powershell_script} }} -Credential (Get-Credential)"
        subprocess.run(command, check=True, shell=True)
        print(f"Installation initiated on {computer}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to initiate installation on {computer}: {e}")

def main():
    for computer in computers:
        run_remote_installation(computer)
        time.sleep(2)  # Small delay between installations

if __name__ == "__main__":
    main()
