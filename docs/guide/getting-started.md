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
    cd diagram-generator
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
      *(Note: You may need to create a `requirements.txt` file containing `Pillow` and `cairosvg`)*

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

4.  **Check the Output**
    If successful, you will see a confirmation message:
    `✅ Image successfully rendered at: output/diagram.png`

    You can now open the `diagram.png` file in the `output/` folder to see your rendered text.

---
**Next:** [Project Structure](./project-structure.md)\
**Back to index:** [Index](./index.md)
