import os
from core.hasher import hash_file

def scan_directory(path):
    results = {}

    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = hash_file(full_path)

            if file_hash:
                results[full_path] = file_hash

    return results