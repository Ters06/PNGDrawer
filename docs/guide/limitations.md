# PNGDrawer - Known Limitations & Best Practices

This document outlines the known limitations of the current version of the `PNGDrawer` application. Understanding these constraints can help you avoid common issues. Each limitation is linked to a corresponding feature request in our backlog.

| Limitation | Description | Related Backlog Item |
| :--- | :--- | :--- |
| **No Automatic Text Wrapping** | Text within a `label` does not wrap automatically. If a string is wider than its parent node, it will overflow. **Workaround:** You must manually insert newline characters (`\\n`) into your text strings to create line breaks. | [PD-001](https://github.com/user/repo/docs/backlog/specs/PD-001.md) |
| **Global Text Color** | The application uses a single, global default color for all text labels. There is no top-level "theme" setting to change this default for all labels at once. **Workaround:** To style a specific label, you must add the `color` property directly to that `label` object. | [PD-004](https://github.com/user/repo/docs/backlog/specs/PD-004.md) |
| **Implicit Layering** | The stacking order of elements (which element appears on top) is determined by their order in the `nodes.json` array. Elements that appear later in the array are drawn on top of elements that appear earlier. **Workaround:** To place an element on top of another, ensure its definition comes *after* the element it should cover. | `N/A` (This is considered a core behavior, but is important to document) |
| **No Dedicated Tag/Overlay System** | The application does not have a built-in feature for adding corner tags or badges to nodes. **Workaround:** This can be achieved by creating a second, smaller shape and using relative placement to position it over the corner of the parent node. See the [Cookbook](./cookbook.md) for a detailed recipe. | [PD-003](https://github.com/user/repo/docs/backlog/specs/PD-003.md) |
