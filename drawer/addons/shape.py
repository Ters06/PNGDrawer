# drawer/addons/shape.py
from PIL import ImageDraw
from .base import Base

class Shape(Base):
    """Draws all 'shape' type nodes."""
    def run(self):
        shape_nodes = [n for n in self.config.get('nodes', []) if n.get('type') == 'shape']
        sorted_shapes = sorted(shape_nodes, key=lambda n: n.get('layer', 0))
        
        for node in sorted_shapes:
            pos = self.renderer.final_positions.get(node['id'])
            if not pos: continue
            
            x, y = pos
            w, h = self.renderer.object_bboxes[node['id']]
            if node.get('shape') == 'rounded_rectangle':
                self.draw.rounded_rectangle(
                    [x, y, x + w, y + h], 
                    radius=node.get('radius', 15) * self.scale_factor, 
                    fill=node.get('color')
                )
