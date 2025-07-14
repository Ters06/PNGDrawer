# PNGDrawer Application - Feature Backlog

**Last Updated:** 2025-07-14

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

### Product Backlog

| ID | Feature Name & Summary | Priority | Status | Epic | Details |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PD-001** | **Automatic Text Wrapping in Nodes** <br/> *Currently, long text strings in `label` properties overflow their parent shape. This requires manual insertion of `\\n` newline characters. This feature will enable automatic text wrapping based on the node's width.* | 🔴 High | 📋 To Do | Core Rendering Engine | [Spec: PD-001](./specs/PD-001.md) |
| **PD-002** | **Advanced Edge Anchor Points** <br/> *The self-referencing iteration arrow was initially drawn inside its node. This feature will add more granular anchor points (e.g., `top_right`, `bottom_left`) to ensure edges always render externally and predictably.* | 🔴 High | 📋 To Do | Core Rendering Engine | [Spec: PD-002](./specs/PD-002.md) |
| **PD-003** | **Node Overlay & Tagging System** <br/> *Placing the "Out of scope" tag required a separate shape with careful relative positioning. This feature will add a dedicated `overlays` array to nodes for easily adding corner tags with predefined styles.* | 🟡 Medium | 📋 To Do | Node Styling | [Spec: PD-003](./specs/PD-003.md) |
| **PD-004** | **Rich Label Styling** <br/> *A workaround was needed to make header titles white. This feature will expand the `label` object to accept its own rich styling properties (e.g., `font_color`, `font_weight`) independent of the global text color.* | 🟡 Medium | 📋 To Do | Node Styling | [Spec: PD-004](./specs/PD-004.md) |
| **PD-005** | **Theme & Color Palette Support** <br/> *Colors are currently hardcoded. This will introduce a `themes.json` definition file where users can define color palettes (e.g., "primary", "accent_1") and reference them in node definitions for consistency.* | 🟢 Low | 📋 To Do | Theming | [Spec: PD-005](./specs/PD-005.md) |
| **PD-006** | **Interactive Web-Based Editor** <br/> *Diagrams are currently defined only via JSON files. This epic would create a WYSIWYG web interface for building diagrams, which would generate the corresponding JSON definitions automatically.* | 🟢 Low | 🧊 Icebox | UI/UX | [Spec: PD-006](./specs/PD-006.md) |
