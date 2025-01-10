import psutil
import winrm
import concurrent.futures

# List of IPs for 50 computers
computer_ips = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3",  # Add all 50 IPs here
]

# Admin credentials
username = "admin_user"
password = "your_password"

# PowerShell script to scan disk for security issues
powershell_script = """
$diskDrives = Get-WmiObject Win32_LogicalDisk
foreach ($drive in $diskDrives) {
    Write-Output "Drive: $($drive.DeviceID)"
    Write-Output "Free Space: $($drive.FreeSpace / 1GB) GB"
    Write-Output "Total Size: $($drive.Size / 1GB) GB"
    if ($drive.FreeSpace / $drive.Size -lt 0.1) {
        Write-Output "WARNING: Disk space critically low on $($drive.DeviceID)"
    } else {
        Write-Output "Disk space is sufficient on $($drive.DeviceID)"
    }
}
"""

def run_local_scan():
    """
    Perform a local scan on the current machine.
    """
    print("Running local disk security scan...")
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"Drive: {partition.device}")
        print(f"Free Space: {usage.free / 1e9:.2f} GB")
        print(f"Total Size: {usage.total / 1e9:.2f} GB")
        if usage.free / usage.total < 0.1:
            print(f"WARNING: Disk space critically low on {partition.device}")
        else:
            print(f"Disk space is sufficient on {partition.device}")

def run_remote_scan(ip):
    """
    Perform a disk security scan on a remote machine using PowerShell.
    """
    try:
        # Create a WinRM session
        session = winrm.Session(f'http://{ip}:5985/wsman', auth=(username, password))
        response = session.run_ps(powershell_script)
        
        if response.status_code == 0:
            print(f"Scan results for {ip}:\n{response.std_out.decode()}")
        else:
            print(f"Error scanning {ip}:\n{response.std_err.decode()}")
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")

def main():
    # Run a local scan on this machine
    run_local_scan()

    # Run remote scans on the list of computers
    print("\nStarting remote scans on 50 computers...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(run_remote_scan, computer_ips)

if __name__ == "__main__":
    main()
