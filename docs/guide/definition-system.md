# Guide: The Definition System

The application uses a powerful, segmented system for defining diagrams. Instead of a single, monolithic configuration file, each diagram is described by a collection of small, focused JSON files within its own dedicated folder.

## Diagram Folder

Every diagram you create must have its own subdirectory inside the `definitions/` folder. The name of this folder becomes the diagram's identifier, which you pass to the `run.py` script.

For example, a diagram named `my-corp-network` would have the following structure:

```
definitions/
└── my-corp-network/
    ├── canvas.json
    ├── nodes.json
    ├── edges.json
    ├── icons.json
    └── ... (other .json files)
```

## The JSON Files

The renderer automatically loads and combines all `.json` files found within a diagram's folder. While you can name the files anything you like, the following conventions are recommended as they map directly to the application's logic.

-   **`canvas.json`**: Defines the global properties of the drawing canvas, such as its size and background color.
-   **`nodes.json`**: The core file where you define all the visual objects (icons, shapes, text) that will appear on the diagram.
-   **`edges.json`**: Defines all the connections (lines and arrows) between the nodes.
-   **`icons.json`**: A mapping file that links a simple, reusable ID to a specific icon file path within the `icons/` directory. This is highly recommended for keeping your `nodes.json` clean.
-   **`layout.json`** (Optional): A file to define special layout rules for positioning objects relative to each other, which can be useful for creating non-standard alignments.

This segmented approach allows you to manage complex diagrams easily by keeping related definitions separate and focused.

---
**Next:** [Placement System](./placement-system.md)\
**Back to index:** [Index](./index.md)
