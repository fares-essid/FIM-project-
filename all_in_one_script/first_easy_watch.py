import hashlib
import os 
import time
import shutil 

MONITOR_PATH = "/home/kali/project/monitor_folder"
VAULT_PATH = "/home/kali/project/.vault"

def hashing(path):
    sha256_hash = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None 

def curent_state(path):
    state = {}
    for filename in os.listdir(path):
        if filename == ".vault":
            continue
        path_x = os.path.join(path, filename)
        if os.path.isfile(path_x):
            h = hashing(path_x)
            if h:
                state[filename] = h
    return state

def create_initial_baseline(folder_path):
    if not os.path.exists(VAULT_PATH):
        os.makedirs(VAULT_PATH)
        print(f"[*] Created hidden vault at {VAULT_PATH}")

    initial_data = {}
    for filename in os.listdir(folder_path):
        if filename == ".vault":
            continue
        path_x = os.path.join(folder_path, filename)
        if os.path.isfile(path_x):
            h = hashing(path_x)
            initial_data[filename] = h
            shutil.copy2(path_x, os.path.join(VAULT_PATH, filename))
    return initial_data

def monitor_folder(folder_path):
    master_baseline = create_initial_baseline(folder_path)
    print(f"[*] Initial Baseline created for {len(master_baseline)} files.")
    print("[*] Monitoring started... Press Ctrl+C to stop.")

    while True:
        time.sleep(2) 
        now_state = curent_state(folder_path)
        
        for filename, current_hash in now_state.items():

            if filename not in master_baseline:
                print(f"[!] ALERT: Unauthorized File: {filename}")
                os.remove(os.path.join(folder_path, filename))
                print(f"[+] ACTION: Unauthorized file removed.")
            

            elif current_hash != master_baseline[filename]:
                print(f"[!] ALERT: Modification detected in: {filename}")
                shutil.copy2(os.path.join(VAULT_PATH, filename), os.path.join(folder_path, filename))
                print(f"[+] ACTION: File restored from vault.")


        for filename in master_baseline:
            if filename not in now_state:
                print(f"[!] ALERT: File Deleted: {filename}")
                shutil.copy2(os.path.join(VAULT_PATH, filename), os.path.join(folder_path, filename))
                print(f"[+] ACTION: File recovered from vault.")

if __name__ == "__main__":    
    monitor_folder(MONITOR_PATH)