import os
import subprocess


def install_software(software_list):
    """install a list of software applications."""

    for software, command in software_list():
        try:
            print(f"Installing {software}...")
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{software} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {software}. Error: {e}")


def main():
     software_list = {
        "7-Zip": r'start /wait "" "7zip_installer.exe" /S'
        # Add more software and their silent installation commands here
    }
     
     install_software(software_list)


if__name__== "__main__": # type: ignore
main()
