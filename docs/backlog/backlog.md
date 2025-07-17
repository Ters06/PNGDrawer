# PNGDrawer Application - Feature Backlog

**Last Updated:** 2025-07-17

This document tracks proposed features, enhancements, and bug fixes for the PNGDrawer application. The backlog is prioritized based on user impact and development effort, helping to guide the future development roadmap.

---

### Legend & Status Key

* **Priority:**
    * 🔴 **High:** Critical for core functionality or major user pain point.
    * 🟡 **Medium:** Important enhancement that improves user experience.
    * 🟢 **Low:** Nice-to-have feature or minor improvement.
* **Status:**
    * 📋 **To Do:** Prioritized and ready for development.
    * ⏳ **In Progress:** Actively being worked on.
    * ✅ **Done:** Completed and deployed.
    * 🧊 **Icebox:** Deprioritized or on hold for future consideration.
* **Epic:** The larger feature group or module this item belongs to.

---

### Active Backlog

| ID         | Feature Name & Summary                                                                                                                                                                                          | Priority | Status | Epic                  | Details                               |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----- | :-------------------- | :------------------------------------ |
| **PD-007** | **Advanced Connection Curve Control** <br/> *The `bend` property for curves is not intuitive. This feature will provide more precise control over connection paths, especially for self-referencing loops.* | 🔴 High  | 📋 To Do | Core Rendering Engine | [Spec: PD-008](./specs/PD-008.md) |
| **PD-002** | **Node Overlay & Tagging System** <br/> *Placing the "Out of scope" tag required a separate shape with careful relative positioning. This feature will add a dedicated `overlays` array to nodes for easily adding corner tags with predefined styles.* | 🟡 Medium | 📋 To Do | Node Styling          | [Spec: PD-003](./specs/PD-003.md) |
| **PD-006** | **Rich Edge Label Styling** <br/> *Labels on edges currently lack styling options. This will enable the same rich text styling for edge labels (`color`, `font_weight`, etc.) as is available for node labels.* | 🟡 Medium | 📋 To Do | Edge Styling          | [Spec: PD-007](./specs/PD-007.md) |
| **PD-003** | **Theme & Color Palette Support** <br/> *Colors are currently hardcoded. This will introduce a `themes.json` definition file where users can define color palettes (e.g., "primary", "accent_1") and reference them in node definitions for consistency.* | 🟢 Low   | 📋 To Do | Theming               | [Spec: PD-005](./specs/PD-005.md) |
| **PD-008** | **Explicit Layering System** <br/> *The current layering is implicit based on definition order. This feature will make the existing `layer` property functional by sorting nodes before rendering.* | 🟢 Low   | 📋 To Do | Core Rendering Engine | [Spec: PD-009](./specs/PD-009.md) |

---

### Completed Items

| ID         | Feature Name & Summary                                                                                                                                                                                                                          | Priority | Status | Epic                  | Details                               |
| :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----- | :-------------------- | :------------------------------------ |
| **PD-001** | **Automatic Text Wrapping in Nodes** <br/> *Long text strings in `label` properties now wrap automatically based on node width, controlled by the `wrapping` and `text_align` properties. This removes the need for manual `\\\\n` characters.* | 🔴 High  | ✅ Done | Core Rendering Engine | [Spec: PD-001](./specs/PD-001.md) |
| **PD-004** | **Rich Label Styling** <br/> *The `label` object now accepts its own rich styling properties (`color`, `font_weight`, `font_style`, `font_size`), allowing labels to be styled independently of global settings.* | 🟡 Medium | ✅ Done | Node Styling          | [Spec: PD-004](./specs/PD-004.md) |
