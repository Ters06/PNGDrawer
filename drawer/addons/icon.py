# drawer/addons/icon.py
from PIL import ImageDraw
from .base import Base

class Icon(Base):
    """Pastes all 'icon' type nodes onto the canvas."""
    def run(self):
        icon_nodes = [n for n in self.config.get('nodes', []) if n.get('type') == 'icon']
        sorted_icons = sorted(icon_nodes, key=lambda n: n.get('layer', 1))

        for node in sorted_icons:
            pos = self.renderer.final_positions.get(node['id'])
            if not pos: continue

            icon_img = self.renderer.loaded_images.get(node['id'])
            if icon_img:
                self.image.paste(icon_img, pos, icon_img)
            else:
                x, y = pos
                w, h = self.renderer.object_bboxes[node['id']]
                self.draw.rectangle([x,y, x+w, y+h], fill="#CCCCCC", outline="red", width=2)
