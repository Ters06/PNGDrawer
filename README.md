# PNGDrawer - A Declarative Diagram Renderer

PNGDrawer is an application that generates high-quality PNG diagrams from a set of simple, declarative JSON files. It allows you to define complex layouts, connections, and styles using a "diagram as code" approach, ensuring your documentation is version-controllable and easy to maintain.

The rendering engine is built with Python and the Pillow library, using an addon-based architecture that makes it highly extensible.

![Workflow Diagram](docs/images/workflow.svg)

---

## Features

- **Declarative JSON Definitions**: Describe every aspect of your diagram—from canvas size to object placement—in simple JSON files.
- **Precise Layout Engine**: Position objects absolutely, relative to the canvas boundaries, or relative to each other using a powerful anchor and offset system.
- **Generic Properties**: Define labels and borders on any object type that supports them (icons, shapes, edges).
- **Layering**: Control the stacking order of objects to create complex, overlapping designs.
- **High-Quality Rendering**: Uses a 4x supersampling technique to produce smooth, anti-aliased lines and crisp text.
- **Vector Icon Support**: Directly uses SVG icons for scalable, high-quality graphics. **Note:** You must provide your own icon files.
- **Flexible Connections**: Draw straight, curved, or S-shaped lines with solid, dashed, or dotted styles, and control arrow direction.
- **Modular Addon Architecture**: The core rendering engine is built on a plugin-like system, making it easy to add new features.

---

## Quick Start

1.  **Gather Icons**: This project does not include icons. You must place your own `.svg` or `.png` files into the `icons/` directory.
2.  **Define your diagram**: Create a new folder inside the `definitions/` directory (e.g., `my-new-diagram`). Inside it, create the necessary `.json` files to describe your diagram.
3.  **Run the application**: From the project root, execute the `run.py` script, passing the name of your definition folder.

    ```bash
    python3 run.py my-new-diagram
    ```

4.  **Find your output**: The final `my-new-diagram.png` will be saved in the `output/` directory.

---

## Using with Generative AI

To accelerate the creation of diagram definitions, you can use a generative AI. A compact guide detailing the application's JSON schema is provided in the `docs/` folder.

**File**: `docs/genAI_compact_guide.md`

### How to Use

1.  **Copy the Guide**: Open the `genAI_compact_guide.md` file and copy its entire content.
2.  **Provide Context to the AI**: Paste the copied guide as a preamble or system prompt to your chosen generative AI. This teaches the AI the rules of the system.
3.  **Make Your Request**: After providing the context, make a clear request for the diagram you want. The AI will generate all the necessary JSON files.
4.  **Manual Step: Update Icon Paths**: The AI will generate an `icons.json` file with logical `icon_id`s but will use **placeholder paths**. You must **manually edit `icons.json`** and replace these placeholders with the correct relative paths to the icon files you have placed in your `icons/` directory.

### Example Prompt

> (Paste the entire content of genAI_compact_guide.md here)
>
> ---
>
> Now, acting as an expert in this system, please generate the complete set of JSON files for a simple diagram showing a user icon connecting to a web server, which then connects to a database.

---

## Documentation

For a complete explanation of all features, file formats, and advanced usage, please refer to the **[Full User Guide](docs/guide/index.md)**.

---

## Project Roadmap & Feature Backlog

This project uses a structured backlog to manage and prioritize the development of new features for the `PNGDrawer` application. This approach ensures that development is transparent and focuses on the most impactful improvements for users.

Our backlog is organized into two main types of documents:

1. **The Main Backlog Page:** This is the central hub for all proposed features. It provides a high-level overview of each item, its priority, status, and the larger epic it belongs to.
   * [View the Main Feature Backlog](./docs/backlog/backlog.md)

2. **Detailed Specification Pages:** Each item in the main backlog links to a detailed "spec" page. These pages provide in-depth information about a specific feature, including:
   * A clear **Problem Statement** explaining the "why" behind the feature.
   * A **Proposed Solution** detailing the "what" and "how".
   * **Technical Details** for implementation.
   * **Acceptance Criteria** to define what "done" looks like.
   * [Browse all Feature Specifications](./docs/backlog/specs/)

This system allows anyone to understand the current state of the project, the direction it's heading, and the detailed thinking behind each proposed change.
