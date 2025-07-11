# drawer/addons/shape.py
import math
from .base import Base
from ..models.node import ShapeObject
from .utils import draw_dashed_path

class Shape(Base):
    """Draws all ShapeObject instances, with full support for custom borders."""
    def run(self):
        shape_nodes = [n for n in self.renderer.nodes if isinstance(n, ShapeObject)]
        sorted_shapes = sorted(shape_nodes, key=lambda n: n.layer)
        self.logger.debug(f"Found {len(sorted_shapes)} shape nodes to draw.")
        
        for node in sorted_shapes:
            self.logger.debug(f"Drawing shape '{node.id}' at position {node.position}")
            x, y = node.position
            w, h = node.bbox
            
            if node.shape == 'rounded_rectangle':
                radius = node.radius * self.scale_factor if node.radius else 15 * self.scale_factor
                
                # --- FIX: Handle 'none' as a transparent fill ---
                fill_color = node.color if node.color != "none" else None
                
                # 1. Draw the fill
                if fill_color:
                    self.draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill_color)

                # 2. Draw the border if it exists
                if node.border:
                    border_color = node.border.get('color', 'black')
                    border_width = int(node.border.get('width', 1) * self.scale_factor)
                    border_type = node.border.get('type', 'solid')

                    # For solid borders, Pillow can draw them directly on the shape
                    if border_type == 'solid':
                        self.draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, outline=border_color, width=border_width)
                    else:
                        # For dashed/dotted, we have to trace the path manually
                        dash_length = 10 * self.scale_factor if border_type == 'dashed' else 2 * self.scale_factor
                        path = self._get_rounded_rect_path(x, y, w, h, radius)
                        draw_dashed_path(self.draw, path, border_color, border_width, dash_length)

    def _get_rounded_rect_path(self, x, y, w, h, r):
        """Generates a list of points representing the path of a rounded rectangle."""
        path = []
        # Top-left to top-right
        path.extend(self._get_arc_points(x + r, y + r, r, 180, 270, 20))
        # Top-right to bottom-right
        path.extend(self._get_arc_points(x + w - r, y + r, r, 270, 360, 20))
        # Bottom-right to bottom-left
        path.extend(self._get_arc_points(x + w - r, y + h - r, r, 0, 90, 20))
        # Bottom-left to top-left
        path.extend(self._get_arc_points(x + r, y + h - r, r, 90, 180, 20))
        path.append(path[0]) # Close the path
        return path

    def _get_arc_points(self, cx, cy, r, start_angle, end_angle, num_segments):
        """Helper to approximate an arc with a series of points."""
        points = []
        for i in range(num_segments + 1):
            angle = math.radians(start_angle + (end_angle - start_angle) * i / num_segments)
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            points.append((px, py))
        return points
