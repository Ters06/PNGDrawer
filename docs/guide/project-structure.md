# Guide: Project Structure

The application uses a specific folder structure to keep diagram definitions, source code, and outputs organized. Understanding this structure is key to using the application effectively.

## Root Directory Layout

Here is the layout of the main `PNGDrawer` directory:

```
PNGDrawer/
├── definitions/
├── docs/
├── icons/
├── output/
├── drawer/
│   ├── addons/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── border.py
│   │   ├── edge.py
│   │   ├── icon.py
│   │   ├── shape.py
│   │   └── text.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── drawable.py
│   │   ├── edge.py
│   │   └── node.py
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── generator.py
│   └── loader.py
└── run.py
```

---

## Modular Design Philosophy

The project is designed to be highly modular, following the principle of **Separation of Concerns**. This means each part of the application has one specific responsibility.

### 1. Data vs. Logic (`definitions/` vs. `drawer/`)

-   **`definitions/`**: Contains only data (JSON files) that describe *what* to draw.
-   **`drawer/`**: This Python package contains only logic that knows *how* to render the diagram.

### 2. The Application Core (`drawer/`)

-   **`config.py`**: Centralizes all directory path management.
-   **`loader.py`**: Parses the JSON definition files for a given diagram.
-   **`cli.py`**: Manages all command-line interaction.
-   **`generator.py`**: The central orchestrator (`ImageRenderer`) that manages the overall rendering process.

### 3. The Data Models (`drawer/models/`)

This directory implements an Object-Oriented approach to the diagram elements. Instead of passing raw dictionaries, the renderer creates "smart" objects.

-   **`drawable.py`**: Defines a `DrawableObject` base class that manages properties common to everything on the canvas, like `id`, `placement`, and `label`.
-   **`node.py` & `edge.py`**: Define specific subclasses like `IconObject`, `ShapeObject`, and `EdgeObject` that inherit from `DrawableObject` and add their own unique properties.

### 4. The Addon Architecture (`drawer/addons/`)

This implements a plugin system for drawing. The `ImageRenderer` delegates all drawing tasks to these specialized addons.

-   **`base.py`**: A base class ensuring all addons have a consistent interface.
-   **Specialized Addons**: Each file (`shape.py`, `icon.py`, `edge.py`, etc.) is responsible for drawing only one type of element. To add a new feature (e.g., a QR code), you would simply create a new `qrcode.py` addon and add it to the sequence in `generator.py`.

---
**Next:** [The Definition System](./definition-system.md)\
**Back to index:** [Index](./index.md)
