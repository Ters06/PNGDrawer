# Guide: Getting Started

This guide will walk you through the initial setup and first run of the diagram renderer application.

## Prerequisites

Before you begin, ensure you have the following installed on your system (preferably a Linux environment like WSL):

- **Python 3.8+**
- **pip** (Python's package installer)
- **Git** (for version control)

## Installation

1.  **Clone the Repository**
    First, get a local copy of the application.
    ```bash
    git clone <your-repository-url>
    cd PNGDrawer
    ```

2.  **Install Dependencies**
    The application relies on a few Python packages and system libraries.

    - **System Libraries (for SVG support):**
      ```bash
      sudo apt-get update
      sudo apt-get install -y libcairo2-dev libgirepository1.0-dev fonts-dejavu
      ```

    - **Python Packages:**
      ```bash
      pip install -r requirements.txt
      ```

3.  **Gather Your Icons**
    This project does **not** ship with a set of icons. You must find and place your own `.svg` or `.png` icon files into the `icons/` directory. You can create subdirectories (e.g., `icons/azure/`, `icons/fortinet/`) to keep them organized. Official icon sets from vendors like Microsoft Azure or Fortinet are a great place to start.

## Your First Diagram

1.  **Create a Definition Folder**
    All diagrams are defined within a dedicated folder inside the `definitions/` directory.
    ```bash
    mkdir definitions/my-first-diagram
    ```

2.  **Define a Node**
    Create a file named `definitions/my-first-diagram/nodes.json` and add a simple object.
    ```json
    [
      {
        "id": "hello_world_text",
        "type": "text",
        "text": "Hello, Diagram!",
        "placement": {
          "type": "absolute",
          "x": 50,
          "y": 50
        }
      }
    ]
    ```

3.  **Run the Renderer**
    From the project's root directory, execute the `run.py` script and pass the name of your new folder.
    ```bash
    python3 run.py my-first-diagram
    ```

## Command-Line Options

The application supports several command-line arguments to modify its behavior.

### Help

You can view all available commands and their descriptions by running the script with the `-h` or `--help` flag.

```bash
python3 run.py --help
```

### Debug Mode

By default, the application only shows high-level informational messages. If you encounter an issue or want to see the detailed step-by-step process of how your diagram is being rendered, you can enable debug mode.

Use the `-d` or `--debug` flag to see a verbose log of the entire process.

```bash
python3 run.py my-first-diagram --debug
```

---
**Next:** [Cookbook](./cookbook.md)\
**Back to index:** [Index](./index.md)
