# drawer/addons/icon.py
from .base import Base
from ..models.node import IconObject

class Icon(Base):
    """Pastes all IconObject instances onto the canvas."""
    def run(self):
        icon_nodes = [n for n in self.renderer.nodes if isinstance(n, IconObject)]
        sorted_icons = sorted(icon_nodes, key=lambda n: n.layer)
        self.logger.debug(f"Found {len(sorted_icons)} icon nodes to draw.")

        for node in sorted_icons:
            if hasattr(node, 'loaded_image'):
                self.logger.debug(f"Drawing icon '{node.id}' at position {node.position}")
                self.image.paste(node.loaded_image, node.position, node.loaded_image)
            else:
                self.logger.warning(f"No loaded image found for icon '{node.id}'. Drawing placeholder.")
                x, y = node.position; w, h = node.bbox
                self.draw.rectangle([x,y, x+w, y+h], fill="#CCCCCC", outline="red", width=2)
