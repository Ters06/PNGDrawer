# drawer/loader.py
import json
from pathlib import Path

def load_diagram_config(directory: Path) -> dict:
    """
    Loads all .json files from a given directory and merges them
    into a single configuration dictionary.
    """
    if not directory.is_dir():
        raise FileNotFoundError(f"Definition directory not found at '{directory}'")

    config = {}
    for json_file in directory.glob('*.json'):
        # The filename (without .json) becomes the key in the config dict
        key = json_file.stem
        with open(json_file, 'r') as f:
            config[key] = json.load(f)

    return config
