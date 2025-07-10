# Declarative Diagram Renderer

This application generates high-quality PNG diagrams from a set of simple, declarative JSON files. It allows you to define complex layouts, connections, and styles using a "diagram as code" approach, ensuring your documentation is version-controllable and easy to maintain.

The rendering engine is built with Python and the Pillow library, using an addon-based architecture that makes it highly extensible.

![Workflow Diagram](docs/images/workflow.svg)

---

## Features

- **Declarative JSON Definitions**: Describe every aspect of your diagram—from canvas size to object placement—in simple JSON files.
- **Precise Layout Engine**: Position objects absolutely, relative to the canvas boundaries, or relative to each other using a powerful anchor and offset system.
- **Layering**: Control the stacking order of objects to create complex, overlapping designs.
- **High-Quality Rendering**: Uses a 4x supersampling technique to produce smooth, anti-aliased lines and crisp text.
- **Vector Icon Support**: Directly uses SVG icons for scalable, high-quality graphics.
- **Flexible Connections**: Draw straight, curved, or S-shaped lines between any two objects.
- **Modular Addon Architecture**: The core rendering engine is built on a plugin-like system, making it easy to add new features and capabilities.

---

## Quick Start

1.  **Define your diagram**: Create a new folder inside the `definitions/` directory (e.g., `my-new-diagram`). Inside it, create a `nodes.json` and an `edges.json` file to describe your objects and their connections.

2.  **Run the application**: From the project root, execute the `run.py` script, passing the name of your definition folder.

    ```bash
    python3 run.py my-new-diagram
    ```

3.  **Find your output**: The final `my-new-diagram.png` will be saved in the `output/` directory.

---

## Documentation

For a complete explanation of all features, file formats, and advanced usage, please refer to the **[Full User Guide](docs/guide/index.md)**.

The guide provides an exhaustive breakdown of:
- Core concepts and project structure.
- How to define and position objects.
- All connection types (straight, curve, s-curve).
- Advanced layout and layering techniques.
