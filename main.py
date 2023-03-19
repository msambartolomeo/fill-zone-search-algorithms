import json
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Config file argument not found")
        exit(1)
    config_path = sys.argv[1]
    with open(config_path, "r") as f:
        config = json.load(f)
        print(config)
