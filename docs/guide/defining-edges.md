# Guide: Connections (`edges.json`)

The `edges.json` file defines all the connections between your nodes. It is an array of edge objects.

## Properties

-   **`source_id`** (string, required): The `id` of the node where the connection starts.
-   **`target_id`** (string, required): The `id` of the node where the connection ends.
-   **`color`** (string, optional): The color of the line, arrowhead, and label.
-   **`source_anchor`** & **`target_anchor`** (string, optional): The anchor points on the objects.
-   **`connection`** (object, optional): An object that defines the style of the line.
-   **`label`** (string or object, optional): A text label for the edge.
    -   If a **string** is provided, the label is drawn at the default `bottom` position (above the midpoint).
    -   If an **object** is provided, you can specify the position relative to the line's bounding box:
        -   **`text`** (string): The label text.
        -   **`position`** (string): `top`, `bottom`, `left`, `right`, `center`.

## Example
```json
[
  {
    "source_id": "web_vm",
    "target_id": "database",
    "label": {
        "text": "TCP 1433",
        "position": "right"
    },
    "color": "#D9534F"
  }
]
```
![Edge Definition Example](../images/edge_definition_example.svg)