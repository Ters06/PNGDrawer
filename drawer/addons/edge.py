# drawer/addons/edge.py
import math
from PIL import ImageDraw
from .base import Base

class Edge(Base):
    """Draws all connections between nodes, supporting straight, curved, and s-curved lines."""
    def run(self):
        for edge in self.config.get('edges', []):
            start, end = self.renderer.get_edge_endpoints(edge)
            if not start or not end: continue

            line_color = edge.get('color', 'black')
            connection_cfg = edge.get('connection', {})
            line_type = connection_cfg.get('type', 'straight')

            # This list will hold the calculated points of the path
            points = []

            if line_type == 'curve':
                points = self._draw_quadratic_curve(start, end, connection_cfg, line_color)
            elif line_type == 's-curve':
                points = self._draw_cubic_curve(start, end, connection_cfg, line_color)
            else:
                self.draw.line([start, end], fill=line_color, width=2 * self.scale_factor)
                points = [start, end]
            
            # Draw the arrowhead using the last segment of the path for correct orientation
            if len(points) >= 2:
                self._draw_arrowhead(points[-2], points[-1], line_color)

    def _draw_quadratic_curve(self, start, end, config, color):
        """Draws a simple quadratic Bézier curve and returns its points."""
        bend = config.get('bend', 0.5)
        mid_x, mid_y = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        dx, dy = end[0] - start[0], end[1] - start[1]
        
        offset = 100 * bend * self.scale_factor
        control_x = mid_x - offset * dy / (math.hypot(dx, dy) or 1)
        control_y = mid_y + offset * dx / (math.hypot(dx, dy) or 1)
        
        points = []
        for t in range(101):
            t /= 100
            x = (1 - t)**2 * start[0] + 2 * (1 - t) * t * control_x + t**2 * end[0]
            y = (1 - t)**2 * start[1] + 2 * (1 - t) * t * control_y + t**2 * end[1]
            points.append((x, y))
        self.draw.line(points, fill=color, width=2 * self.scale_factor)
        return points
        
    def _draw_cubic_curve(self, start, end, config, color):
        """Draws an S-shaped cubic Bézier curve and returns its points."""
        bend_factors = config.get('bend', [0.5, -0.5])
        bend_start, bend_end = bend_factors[0], bend_factors[1]

        dx, dy = end[0] - start[0], end[1] - start[1]
        hypot = math.hypot(dx, dy) or 1

        # Control point 1
        cp1_base_x, cp1_base_y = start[0] + dx * 0.25, start[1] + dy * 0.25
        offset1 = 75 * bend_start * self.scale_factor
        cp1_x = cp1_base_x - offset1 * dy / hypot
        cp1_y = cp1_base_y + offset1 * dx / hypot

        # Control point 2
        cp2_base_x, cp2_base_y = start[0] + dx * 0.75, start[1] + dy * 0.75
        offset2 = 75 * bend_end * self.scale_factor
        cp2_x = cp2_base_x - offset2 * dy / hypot
        cp2_y = cp2_base_y + offset2 * dx / hypot

        points = []
        for t in range(101):
            t /= 100
            omt = 1 - t
            x = (omt**3 * start[0] + 
                 3 * omt**2 * t * cp1_x + 
                 3 * omt * t**2 * cp2_x + 
                 t**3 * end[0])
            y = (omt**3 * start[1] + 
                 3 * omt**2 * t * cp1_y + 
                 3 * omt * t**2 * cp2_y + 
                 t**3 * end[1])
            points.append((x, y))
        self.draw.line(points, fill=color, width=2 * self.scale_factor)
        return points

    def _draw_arrowhead(self, start_point, end_point, color):
        """Draws an arrowhead at the end of a line segment."""
        arrow_size = 15 * self.scale_factor
        try:
            # The angle is now based on the final segment of the curve/line
            angle = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
            
            p1 = (end_point[0] - arrow_size * math.cos(angle - math.pi / 6),
                  end_point[1] - arrow_size * math.sin(angle - math.pi / 6))
            p2 = (end_point[0] - arrow_size * math.cos(angle + math.pi / 6),
                  end_point[1] - arrow_size * math.sin(angle + math.pi / 6))
            self.draw.polygon([end_point, p1, p2], fill=color)
        except Exception as e:
            print(f"⚠️ Warning: Could not draw arrowhead. {e}")
