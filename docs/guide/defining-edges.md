# Guide: Connections (`edges.json`)

The `edges.json` file defines all the connections (lines and arrows) between your nodes. It is an array of edge objects.

## Properties

-   **`source_id`** (string, required): The `id` of the node where the connection starts.
-   **`target_id`** (string, required): The `id` of the node where the connection ends.
-   **`color`** (string, optional): The color of the line, arrowhead, and label. Defaults to `black`.
-   **`source_anchor`** & **`target_anchor`** (string, optional): The anchor points on the objects. See the [Placement System](./placement-system.md) guide for a full list of valid anchors. Defaults to `right` and `left` respectively.
-   **`connection`** (object, optional): An object that defines the style of the line. See the [Connection Styling](./connection-styles.md) guide for full details.
-   **`label`** (string or object, optional): A text label for the edge. The application will automatically rotate the label to match the line's angle and will draw a background to ensure it is readable.
    -   If a **string** is provided, the label is drawn at the default `bottom` position (above the midpoint).
    -   If an **object** is provided, you can specify the position relative to the line's bounding box:
        -   **`text`** (string): The label text.
        -   **`position`** (string): `top`, `bottom`, `left`, `right`, `center`.

## Example

**`definitions/my-diagram/edges.json`**
```json
[
  {
    "source_id": "web_vm",
    "target_id": "database",
    "label": "TCP 1433",
    "color": "#D9534F",
    "source_anchor": "bottom",
    "target_anchor": "top"
  }
]
```
![Edge Definition Example](../images/edge_definition_example.svg)

---
**Next:** [Connection Styles](./connection-styles.md)\
**Back to index:** [Index](./index.md)
