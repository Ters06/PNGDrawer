# drawer/config.py
from pathlib import Path

# The project root is two levels up from this file (config.py -> drawer/ -> ROOT)
PROJECT_ROOT = Path(__file__).parent.parent
DEFINITIONS_DIR = PROJECT_ROOT / "definitions"
OUTPUT_DIR = PROJECT_ROOT / "output"
ICONS_DIR = PROJECT_ROOT / "icons"
