# drawer/addons/text.py
from PIL import ImageDraw
from .base import Base

class Text(Base):
    """Draws all text elements, including labels for icons and edges."""
    def run(self):
        # Draw labels for icons
        icon_nodes = [n for n in self.config.get('nodes', []) if n.get('type') == 'icon' and 'label' in n]
        for node in icon_nodes:
            pos = self.renderer.final_positions.get(node['id'])
            bbox = self.renderer.object_bboxes.get(node['id'])
            if not pos or not bbox: continue
            
            label_pos = (pos[0] + bbox[0] / 2, pos[1] + bbox[1] + (5 * self.scale_factor))
            self.draw.text(label_pos, node['label'], fill="#000000", font=self.renderer.font, anchor="mt")
            
        # Draw standalone text nodes
        text_nodes = [n for n in self.config.get('nodes', []) if n.get('type') == 'text']
        for node in text_nodes:
            pos = self.renderer.final_positions.get(node['id'])
            if not pos: continue
            self.draw.text(pos, node.get('text'), fill=node.get('color', 'black'), font=self.renderer.font)

        # Draw labels for edges
        for edge in self.config.get('edges', []):
            if 'label' in edge:
                start_pos, end_pos = self.renderer.get_edge_endpoints(edge)
                if not start_pos or not end_pos: continue
                
                mid_point = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2 - (10 * self.scale_factor))
                self.draw.text(mid_point, edge['label'], fill=edge.get('color', 'black'), font=self.renderer.font, anchor="ms")
