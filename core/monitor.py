import time
from core.scanner import scan_directory
from core.database import load_db, save_db
from alerts.alert_manager import alert

def monitor(paths, interval):
    db = load_db()

    while True:
        for path in paths:
            current_state = scan_directory(path)

            for file, hash_val in current_state.items():
                if file not in db:
                    alert(f"[NEW FILE] {file}")

                elif db[file] != hash_val:
                    alert(f"[MODIFIED] {file}")

            for file in db:
                if file not in current_state:
                    alert(f"[DELETED] {file}")

            db.update(current_state)

        save_db(db)
        time.sleep(interval)