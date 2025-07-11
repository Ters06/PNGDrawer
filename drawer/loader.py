# drawer/loader.py
import json
import logging
from pathlib import Path

def load_diagram_config(directory: Path) -> dict:
    """
    Loads all .json files from a given directory and merges them
    into a single configuration dictionary.
    """
    logger = logging.getLogger(__name__)
    
    if not directory.is_dir():
        logger.error(f"Definition directory not found at '{directory}'")
        raise FileNotFoundError(f"Definition directory not found at '{directory}'")

    logger.info(f"Loading diagram configuration from: {directory}")
    config = {}
    json_files_found = list(directory.glob('*.json'))

    if not json_files_found:
        logger.warning(f"No .json definition files found in '{directory}'.")
        return config

    for json_file in json_files_found:
        key = json_file.stem
        logger.debug(f"  > Loading file: {json_file.name} -> as key: '{key}'")
        try:
            with open(json_file, 'r') as f:
                config[key] = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from file {json_file.name}: {e}")
            raise
    
    logger.info("Configuration loading complete.")
    return config
