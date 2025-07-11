# drawer/cli.py
import json
import argparse
import sys
import logging
from .config import DEFINITIONS_DIR
from .loader import load_diagram_config
from .generator import ImageRenderer

def main():
    """Defines the command-line interface and runs the generator."""
    parser = argparse.ArgumentParser(
        description="Generates a PNG diagram from a directory of JSON definition files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "directory_name", 
        help="Name of the diagram directory inside the 'definitions' folder (e.g., 'fortinet-azure-hub-spoke')"
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug logging to see detailed processing steps."
    )
    args = parser.parse_args()

    # Configure logging based on the debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logging.info(f"Processing diagram definition: '{args.directory_name}'")

    definition_dir = DEFINITIONS_DIR / args.directory_name
    
    try:
        config = load_diagram_config(definition_dir)
    except Exception as e:
        logging.error(f"Failed to load diagram configuration: {e}")
        sys.exit(1)

    # Create and run the renderer
    renderer = ImageRenderer(config)
    renderer.render()
