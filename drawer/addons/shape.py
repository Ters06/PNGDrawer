# drawer/addons/shape.py
import math
from .base import Base
from ..models.node import ShapeObject

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
                
                # 1. Draw the fill first
                self.draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=node.color)

                # 2. Draw the border if it exists
                if node.border:
                    border_color = node.border.get('color', 'black')
                    border_width = int(node.border.get('width', 1) * self.scale_factor)
                    border_type = node.border.get('type', 'solid')

                    if border_type == 'solid':
                        self.draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, outline=border_color, width=border_width)
                    else:
                        # For dashed/dotted, we draw the path manually
                        dash_length = 10 * self.scale_factor if border_type == 'dashed' else 2 * self.scale_factor
                        self._draw_dashed_rounded_rect(x, y, w, h, radius, border_color, border_width, dash_length)

    def _draw_dashed_line(self, start, end, color, width, dash_length):
        """Helper to draw a simple dashed line segment."""
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        if length == 0: return
        
        unit_dx, unit_dy = dx / length, dy / length
        
        current_length = 0
        while current_length < length:
            draw_end_length = min(current_length + dash_length, length)
            p_start = (start[0] + unit_dx * current_length, start[1] + unit_dy * current_length)
            p_end = (start[0] + unit_dx * draw_end_length, start[1] + unit_dy * draw_end_length)
            self.draw.line([p_start, p_end], fill=color, width=width)
            current_length += dash_length * 2

    def _draw_dashed_rounded_rect(self, x, y, w, h, r, color, width, dash_length):
        """Draws a dashed border for a rounded rectangle."""
        # Draw the four straight sides
        self._draw_dashed_line((x + r, y), (x + w - r, y), color, width, dash_length)
        self._draw_dashed_line((x + r, y + h), (x + w - r, y + h), color, width, dash_length)
        self._draw_dashed_line((x, y + r), (x, y + h - r), color, width, dash_length)
        self._draw_dashed_line((x + w, y + r), (x + w, y + h - r), color, width, dash_length)

        # Draw the four corner arcs
        self.draw.arc([x, y, x + 2*r, y + 2*r], 180, 270, fill=color, width=width) # Top-left
        self.draw.arc([x + w - 2*r, y, x + w, y + 2*r], 270, 360, fill=color, width=width) # Top-right
        self.draw.arc([x, y + h - 2*r, x + 2*r, y + h], 90, 180, fill=color, width=width) # Bottom-left
        self.draw.arc([x + w - 2*r, y + h - 2*r, x + w, y + h], 0, 90, fill=color, width=width) # Bottom-right
