# Guide: Connection Styling

You can control the style of the lines drawn between objects by adding an optional `connection` object to any edge definition in `edges.json`.

## Line Style

The `style` property controls the appearance of the line itself.

-   **`style`** (string, optional):
    -   `"solid"`: (Default) A solid, continuous line.
    -   `"dashed"`: A line made of long dashes.
    -   `"dotted"`: A line made of small dots (short dashes).

### Example
```json
"connection": {
  "style": "dashed"
}
```
![Dashed Connection Example](../images/connection_dashed_example.svg)

---

## Line Shape

The `type` property controls the path the line takes between two points.

-   **`type`** (string, optional): `"straight"` (default), `"curve"`, or `"s-curve"`.

### Curved Lines
A simple, single-bend (quadratic Bézier) curve.

-   **`type`**: `"curve"`
-   **`bend`** (float, optional): Controls curvature. Positive values bend one way, negative values bend the other. Defaults to `0.5`.

### S-Curved Lines
A more complex S-shaped (cubic Bézier) curve.

-   **`type`**: `"s-curve"`
-   **`bend`** (array of float `[start_bend, end_bend]`, optional): Controls the S-shape. Defaults to `[0.5, -0.5]`.

### Examples
```json
// Simple Curve
"connection": {
  "type": "curve",
  "bend": -0.7
}
```
![Curved Connection Example](../images/connection_curve_example.svg)

```json
// S-Curve
"connection": {
  "type": "s-curve",
  "bend": [0.6, -0.6]
}
```
![S-Curved Connection Example](../images/connection_scurve_example.svg)

---

## Arrow Direction

The `direction` property controls the arrowheads on the line.

-   **`direction`** (string, optional):
    -   `"forward"`: (Default) Draws an arrow from source to target.
    -   `"backward"`: Draws an arrow from target to source.
    -   `"bidirectional"`: Draws arrows on both ends.
    -   `"none"`: Draws a line with no arrowheads.

### Example
```json
"connection": {
  "direction": "bidirectional"
}
```
![Bidirectional Connection Example](../images/connection_bidirectional_example.svg)

---
**Back to index:** [Index](./index.md)
