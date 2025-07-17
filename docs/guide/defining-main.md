# Defining the Main File (`main.json`)

The `main.json` file is the entry point for your diagram's configuration. It contains meta-information and global settings.

## Properties

| Property            | Type   | Description                                                                                                                 | Default       |
| ------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `output_filename`   | string | The name of the output file (without extension). The image will be saved as a `.png`.                                         | `"diagram"`   |
| `default_font_size` | int    | The default font size for all text in the diagram. This value can be overridden by a label's `font_size` property. | `15`          |

## Example

```json
{
    "output_filename": "my-awesome-diagram",
    "default_font_size": 14
}
```

---
**Next:** [Canvas (`canvas.json`)](./defining-canvas.md)\
**Back to index:** [Index](./index.md)