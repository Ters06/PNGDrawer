# Guide: Nodes (`nodes.json`)

The `nodes.json` file is where you define all the visual objects that will appear on your diagram. It is an array of node objects.

## Common Node Properties

All node types share these common properties:

-   **`id`** (string, required): A unique identifier for the node.
-   **`type`** (string, required): `"icon"`, `"shape"`, or `"text"`.
-   **`layer`** (integer, optional): The drawing layer for the object. Higher numbers are drawn on top. Defaults to `1`.
-   **`placement`** (object, required): An object that defines the node's position. See the [Placement System](./placement-system.md) guide for full details.
-   **`label`** (string or object, optional): A text label for the node. This is a generic property available for `icon`, `shape`, and `edge` types.
    -   If a **string** is provided (e.g., `"label": "My Text"`), the label is drawn at the default `bottom` position. This is a shorthand for simple labels.
    -   If an **object** is provided, you can access advanced styling options.

---

## The `label` Object

For advanced styling, the `label` property can be an object with the following properties:

| Property       | Type   | Description                                                                                             | Default         |
| --------------- | ------ | ------------------------------------------------------------------------------------------------------- | -------------- |
| `text`          | string | The text to display.                                                                                    | `""`           |
| `position`      | string | The label's position relative to the node. Ex: `"center"`, `"top"`, `"bottom_left"`.                       | `"center"`     |
| `color`         | string | The text color in hexadecimal format.                                                              | `"#000000"` (Black) |
| `font_size`     | int    | The font size. Overrides `default_font_size` from `main.json`.                                     | `12`           |
| `font_weight`   | string | The font weight. Possible values: `"normal"`, `"bold"`.                                        | `"normal"`     |
| `font_style`    | string | The font style. Possible values: `"normal"`, `"italic"`.                                        | `"normal"`     |
| `wrapping`      | string | Enables automatic text wrapping. `"auto"` to enable, `"none"` to disable.                 | `"auto"`       |
| `text_align`    | string | The horizontal alignment for multi-line text. `"left"`, `"center"`, `"right"`.           | `"center"`     |

> **Note:** For `edge` labels, only the `text` property is currently used. Advanced styling (color, font, wrapping) for edge labels is not yet implemented.

---

## Node Type: `icon`

Draws an SVG or PNG icon.

-   **`icon_id`** (string, required): The ID of the icon from `icons.json`.
-   **`size`** (array of int, optional): `[width, height]` to resize the icon.

### Example
This example shows an icon with a simple string label, which will default to the `bottom` position.

```json
{
  "id": "web_server",
  "type": "icon",
  "icon_id": "azure-vm",
  "label": "Production Server",
  "size": [64, 64],
  "placement": { "type": "absolute", "x": 100, "y": 100 }
}
```
![Simple Label Example](../images/simple_label_example.svg)

---

## Node Type: `shape`

Draws simple geometric shapes.

-   **`shape`** (string, required): Currently supports `"rounded_rectangle"`.
-   **`size`** (array of int, required): `[width, height]` for the shape's dimensions.
-   **`color`** (string, required): The fill color. Can be a hex code or `"none"` for a transparent fill.
-   **`radius`** (integer, optional): Corner radius for `rounded_rectangle`.
-   **`border`** (object, optional): Defines a custom border for the shape.
    -   **`color`** (string): The border color.
    -   **`width`** (integer): The border width in pixels.
    -   **`type`** (string): The border style. Can be `"solid"`, `"dashed"`, or `"dotted"`.

### Example: Shape with Advanced Label and Border
This example shows a shape with a styled, wrapped, left-aligned label, and a custom dashed border, using the full `label` object.

<svg width="320" height="170" xmlns="http://www.w3.org/2000/svg">
    <rect x="10" y="10" width="300" height="150" rx="10" ry="10" fill="#E3F2FD" stroke="#0D6EFD" stroke-width="2" stroke-dasharray="8 4"/>
    <text x="25" y="45" font-family="DejaVu Sans" font-size="16" font-weight="bold" fill="#0B5ED7">This is a long line of text</text>
    <text x="25" y="65" font-family="DejaVu Sans" font-size="16" font-weight="bold" fill="#0B5ED7">that requires automatic</text>
    <text x="25" y="85" font-family="DejaVu Sans" font-size="16" font-weight="bold" fill="#0B5ED7">wrapping to be displayed</text>
    <text x="25" y="105" font-family="DejaVu Sans" font-size="16" font-weight="bold" fill="#0B5ED7">correctly.</text>
</svg>

```json
{
    "id": "vnet_background",
    "type": "shape",
    "shape": "rounded_rectangle",
    "size": [ 300, 150 ],
    "color": "#E3F2FD",
    "border": {
        "color": "#0D6EFD",
        "width": 2,
        "type": "dashed"
    },
    "placement": { "type": "absolute", "x": 50, "y": 50 },
    "label": {
        "text": "This is a long line of text that requires automatic wrapping to be displayed correctly.",
        "position": "center",
        "color": "#0B5ED7",
        "font_size": 16,
        "font_weight": "bold",
        "wrapping": "auto",
        "text_align": "left"
    }
}
```

---

## Node Type: `text`

Draws standalone text. This type does not use the `label` property, as its primary purpose is to display text directly.

-   **`text`** (string, required): The text content to display.
-   **`font_size`** (integer, optional): The font size.
-   **`color`** (string, optional): The color of the text.

### Example
```json
{
  "id": "diagram_title",
  "type": "text",
  "text": "Corporate Network Architecture",
  "font_size": 24,
  "color": "#333333",
  "layer": 3,
  "placement": { "type": "absolute", "x": 20, "y": 20 }
}
```
![Text Node Example](../images/text_node_example.svg)

---
**Next:** [Icons (`icons.json`)](./defining-icons.md)\
**Back to index:** [Index](./index.md)
