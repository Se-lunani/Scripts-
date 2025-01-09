import shutil
import os

def copy_files(source_directory, destination_directory):
    files = os.listdir(source_directory)
    for file in files:
        shutil.copy(os.path.join(source_directory, file), destination_directory)

# Usage
copy_files('/path/to/source_directory', '/path/to/destination_directory')
