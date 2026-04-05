import hashlib
import os 

from time import sleep

def hash_file(file_path):
    sha256_hash= hashlib.sha256()
    try: 
        with open(file_path,"rb") as f :
            for byte_block in iter(lambda:f.read(4096),b""):
                sha256_hash.update(byte_block)
        print(f"File {file_path} hashed successfully.")
        return sha256_hash.hexdigest()
    
    except Exception as e:
        print(f"Error hashing file: {e}")
        return None 
    except PermissionError as pe:
        print(f"Permission denied for file: {file_path}. Error: {pe}")
        return False
    


def permission_file_denied(file_path):
    if  hash_file(file_path) is False:
        sleep(1)
        os.chmod(file_path, 0o644)
        print(f"Permissions for file {file_path} have been updated to allow hashing.")
    hash_file(file_path)