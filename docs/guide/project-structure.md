# Guide: Project Structure

The application uses a specific folder structure to keep diagram definitions, source code, and outputs organized. Understanding this structure is key to using the application effectively.

## Root Directory Layout

Here is the layout of the main `diagram-generator` directory:

```
diagram-generator/
├── definitions/
├── docs/
├── icons/
├── output/
├── drawer/
└── run.py
```

### Folder Descriptions

-   **`definitions/`**
    This is where all your diagram definitions live. Each subdirectory inside `definitions/` represents a single, unique diagram.

-   **`docs/`**
    Contains all project documentation, including this user guide.

-   **`icons/`**
    The central repository for all your SVG and PNG icon files. You can create subdirectories within this folder to organize your icons by vendor or category (e.g., `icons/azure/`, `icons/fortinet/`).

-   **`output/`**
    The default location where all generated PNG diagrams are saved. This folder is created automatically if it doesn't exist.

-   **`drawer/`**
    This is the main Python source package for the application. It contains all the core logic, including the rendering engine and the addon system. You generally won't need to modify these files unless you are extending the application's features.

-   **`run.py`**
    A simple script in the root directory that serves as the main entry point for running the application.

---
**Next:** [The Definition System](./definition-system.md)\
**Back to index:** [Index](./index.md)
