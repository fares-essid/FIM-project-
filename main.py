import yaml
from core.monitor import monitor

def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    config = load_config()

    monitor(
        config["watch_paths"],
        config["scan_interval"]
    )