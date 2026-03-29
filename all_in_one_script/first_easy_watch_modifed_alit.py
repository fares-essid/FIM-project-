import hashlib
import os 
import time
import shutil 

vault_path = "/home/kali/project/.vault"  #any file or directory that starts with a dot . is hidden
folder_to_monitor = "/home/kali/project/monitor_folder"

def hashing(path):
    sha256_hash = hashlib.sha256() #object de hashage interne _hashlib.HASH
    with open(path,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def curent_state(path):
    baseline={}
    for filename in os.listdir(path):
        if filename==".vault":
            continue
        path_x=os.path.join(path,filename)
        if os.path.isfile(path_x):
            hash = hashing(path_x)
            baseline[filename] = hash
    return baseline

def create_intitial_baseline(folder_path):
    if not os.path.exists(vault_path):
        os.makedirs(vault_path)

    initial_data={}
    for filename in os.listdir(folder_path):
        if filename==".vault":
            continue
        path_x=os.path.join(folder_path,filename)
        if os.path.isfile(path_x):
            hash=hashing(path_x)
            initial_data[filename] = hash
            shutil.copy2(path_x,os.path.join(vault_path,filename))
    return initial_data

def monitor_folder(folder_path):
    baseline_ = create_intitial_baseline(folder_path)
    print("Initial Baseline created ")

    while True:
        time.sleep(5) 
        current_state = curent_state(folder_path)
        
        for filename, current_hash in current_state.items():
            if filename not in baseline_:
                print(f"[!] ALERT: New File Created: {filename}")
                os.remove(os.path.join(folder_path,filename))
                print(f"[!] ALERT: New File Created: {filename} has been removed")

            elif current_hash != baseline_[filename]:
                print(f"[!] ALERT: File Modified: {filename}")
                shutil.copy2(os.path.join(vault_path,filename),os.path.join(folder_path,filename))
                print(f"[!] ALERT: File Modified: {filename} has been restored")

        for filename in baseline_:
            if filename not in current_state:
                print(f"[!] ALERT: File Deleted: {filename}")
                shutil.copy2(os.path.join(vault_path,filename),os.path.join(folder_path,filename))
                print(f"[!] ALERT: File Deleted: {filename} has been restored")

        baseline_ = current_state

if __name__ == "__main__":    
    monitor_folder(folder_to_monitor)