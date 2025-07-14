# PNGDrawer Cookbook & Recipes

Welcome to the PNGDrawer Cookbook! This guide provides practical, copy-pasteable solutions for common diagramming patterns.

### Table of Contents
1. [Recipe: Creating a Self-Referencing Loop](#recipe-creating-a-self-referencing-loop)
2. [Recipe: Creating Overlapping Corner Tags](#recipe-creating-overlapping-corner-tags)
3. [Recipe: Styling Header Text](#recipe-styling-header-text)

---

### Recipe: Creating a Self-Referencing Loop
**Goal:** Draw an arrow that loops from one corner of a node back to another corner on the same node, staying entirely outside the node's border. This is ideal for showing iterations.

**Challenge:** A simple loop can render inside the node. The key is to use corner anchors (`top_right`, `bottom_right`) to force the path outside the shape.

**Result:**
<svg width="200" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="25" width="160" height="100" rx="10" ry="10" fill="#FFFFFF" stroke="#ADB5BD" stroke-width="1"/>
  <text x="100" y="75" font-family="sans-serif" font-size="14" text-anchor="middle" fill="#343A40">Iteration</text>
  <path d="M 180 125 Q 220 95, 180 65" stroke="#343A40" stroke-width="1.5" fill="none" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#343A40"/>
    </marker>
  </defs>
</svg>

**`edges.json` Configuration:**
```json
[
    {
        "source_id": "my_node_id",
        "target_id": "my_node_id",
        "source_anchor": "bottom_right",
        "target_anchor": "top_right",
        "connection": {
            "type": "curve",
            "bend": -0.8
        }
    }
]
```

---

### Recipe: Creating Overlapping Corner Tags
**Goal:** Add a small, styled tag (like "Out of scope") that overlaps a corner of a parent node.

**Challenge:** There is no dedicated "tag" feature. The solution is to create a second, smaller shape and use relative placement with `self_anchor: "center"` to position it precisely over the corner of the parent node. The tag node must appear *after* the parent node in `nodes.json` to render on top.

**Result:**
<svg width="250" height="150" xmlns="http://www.w3.org/2000/svg">
  <g>
    <rect x="25" y="25" width="200" height="100" rx="10" ry="10" fill="#FFFFFF" stroke="#ADB5BD" stroke-width="1"/>
    <text x="125" y="75" font-family="sans-serif" font-size="14" text-anchor="middle" fill="#343A40">Main Content</text>
  </g>
  <g>
    <rect x="25" y="25" width="100" height="25" rx="12.5" ry="12.5" fill="#F8D7DA" stroke="none"/>
    <text x="75" y="42" font-family="sans-serif" font-size="12" text-anchor="middle" fill="#D9534F">Out of scope</text>
  </g>
</svg>


**`nodes.json` Configuration:**
```json
[
    {
        "id": "parent_box",
        "type": "shape",
        "shape": "rounded_rectangle",
        "color": "white",
        "size": [ 200, 100 ],
        "layer": 1,
        "label": { "text": "Main Content" }
    },
    {
        "id": "out_of_scope_tag",
        "type": "shape",
        "shape": "rounded_rectangle",
        "color": "#F8D7DA",
        "size": [ 100, 25 ],
        "radius": 12.5,
        "layer": 2,
        "placement": {
            "type": "relative",
            "target_id": "parent_box",
            "target_anchor": "top_left",
            "self_anchor": "center"
        },
        "label": {
            "text": "Out of scope",
            "color": "#D9534F"
        }
    }
]
```
---

### Recipe: Styling Header Text
**Goal:** Create a colored header box with white text, overriding the default dark text color.

**Challenge:** The `label` object does not inherit color from its parent shape. You must explicitly set the `color` property inside the `label` object itself.

**Result:**
<svg width="250" height="80" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="15" width="200" height="50" rx="10" ry="10" fill="#6C757D" stroke="none"/>
  <text x="125" y="48" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle" fill="#FFFFFF">Header</text>
</svg>

**`nodes.json` Configuration:**
```json
{
    "id": "my_header",
    "type": "shape",
    "shape": "rounded_rectangle",
    "color": "#6C757D",
    "size": [ 200, 50 ],
    "label": {
        "text": "Header",
        "position": "center",
        "color": "#FFFFFF",
        "font_size": 20,
        "font_weight": "bold"
    }
}
```