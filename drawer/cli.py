# drawer/cli.py
import argparse
import sys
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
        help="Name of the diagram directory inside the 'definitions' folder.\n(e.g., 'azure-outbound-flow')"
    )
    args = parser.parse_args()

    # Construct the full path to the definition directory
    definition_dir = DEFINITIONS_DIR / args.directory_name
    
    try:
        config = load_diagram_config(definition_dir)
    except Exception as e:
        print(f"❌ Error: Failed to load diagram configuration. {e}")
        sys.exit(1)

    # Create and run the renderer
    renderer = ImageRenderer(config)
    renderer.render()
