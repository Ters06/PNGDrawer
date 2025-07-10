# Guide: Icons (`icons.json`)

> **Important Note:** This project does not include a library of icons. You are responsible for sourcing your own icon files (in `.svg` or `.png` format) and placing them inside the `icons/` directory.

The `icons.json` file provides a clean and maintainable way to manage your icon assets. It acts as a central mapping where you associate a simple, reusable ID with the actual file path of an icon.

This abstraction is highly recommended. It allows you to change an icon's file path in one place, and every node that uses its ID will be automatically updated. It also keeps your `nodes.json` file cleaner and focused on object definition rather than asset paths.

## Structure

The file is a simple JSON object where:
-   The **key** is the `icon_id` you will use in `nodes.json`.
-   The **value** is the relative path to the icon file, starting from the `icons/` directory.

## Example

**`definitions/my-diagram/icons.json`**
```json
{
  "azure-vm": "azure/compute/vm.svg",
  "azure-lb": "azure/network/load_balancer.svg",
  "fortinet-fw": "fortinet/firewall.svg",
  "generic-internet": "generic/internet.svg",
  "onprem-server": "onprem/server.png"
}
```

### Usage in `nodes.json`

You would then use these IDs in your `nodes.json` file like this:

```json
// ... inside nodes.json
{
  "id": "web_server_1",
  "type": "icon",
  "icon_id": "azure-vm", // <-- This ID maps to the path in icons.json
  "label": "Web Server 1",
  "size": [64, 64],
  "placement": { "...": "..." }
}
```

---
**Next:** [Connections (`edges.json`)](./defining-edges.md)\
**Back to index:** [Index](./index.md)
