# drawer/addons/edge.py
import math
from .base import Base
from .utils import draw_dashed_path

class Edge(Base):
    """Draws all connections between nodes, supporting various styles and directions."""
    def run(self):
        for edge in self.renderer.edges:
            self.logger.debug(f"Drawing edge from '{edge.source_id}' to '{edge.target_id}'")
            start, end = self.renderer.get_edge_endpoints(edge)
            if not start or not end: continue

            line_color = edge.color
            connection_cfg = edge.connection_config
            line_type = connection_cfg.get('type', 'straight')
            line_style = connection_cfg.get('style', 'solid')

            points = []
            if line_type == 'curve':
                points = self._get_quadratic_curve_points(start, end, connection_cfg)
            elif line_type == 's-curve':
                points = self._get_cubic_curve_points(start, end, connection_cfg)
            else:
                points = [start, end]
            
            self._draw_line_with_style(points, line_color, line_style)
            
            direction = connection_cfg.get('direction', 'forward')
            if direction in ['forward', 'bidirectional']:
                self._draw_arrowhead(points[-2], points[-1], line_color)
            if direction in ['backward', 'bidirectional']:
                self._draw_arrowhead(points[1], points[0], line_color)

    def _draw_line_with_style(self, points, color, style):
        """Draws a line (straight or curved) with a given style."""
        if style == 'solid':
            self.draw.line(points, fill=color, width=2 * self.scale_factor)
        else:
            dash_length = 10 * self.scale_factor if style == 'dashed' else 2 * self.scale_factor
            draw_dashed_path(self.draw, points, color, 2 * self.scale_factor, dash_length)

    def _get_quadratic_curve_points(self, start, end, config):
        """Calculates points for a quadratic Bézier curve."""
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
        return points
        
    def _get_cubic_curve_points(self, start, end, config):
        """Calculates points for a cubic Bézier curve."""
        bend_factors = config.get('bend', [0.5, -0.5])
        bend_start, bend_end = bend_factors[0], bend_factors[1]

        dx, dy = end[0] - start[0], end[1] - start[1]
        hypot = math.hypot(dx, dy) or 1

        cp1_base_x, cp1_base_y = start[0] + dx * 0.25, start[1] + dy * 0.25
        offset1 = 75 * bend_start * self.scale_factor
        cp1_x = cp1_base_x - offset1 * dy / hypot
        cp1_y = cp1_base_y + offset1 * dx / hypot

        cp2_base_x, cp2_base_y = start[0] + dx * 0.75, start[1] + dy * 0.75
        offset2 = 75 * bend_end * self.scale_factor
        cp2_x = cp2_base_x - offset2 * dy / hypot
        cp2_y = cp2_base_y + offset2 * dx / hypot

        points = []
        for t in range(101):
            t /= 100
            omt = 1 - t
            x = (omt**3 * start[0] + 3 * omt**2 * t * cp1_x + 3 * omt * t**2 * cp2_x + t**3 * end[0])
            y = (omt**3 * start[1] + 3 * omt**2 * t * cp1_y + 3 * omt * t**2 * cp2_y + t**3 * end[1])
            points.append((x, y))
        return points

    def _draw_arrowhead(self, start_point, end_point, color):
        """Draws an arrowhead at the end of a line segment."""
        arrow_size = 15 * self.scale_factor
        try:
            angle = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
            
            p1 = (end_point[0] - arrow_size * math.cos(angle - math.pi / 6),
                  end_point[1] - arrow_size * math.sin(angle - math.pi / 6))
            p2 = (end_point[0] - arrow_size * math.cos(angle + math.pi / 6),
                  end_point[1] - arrow_size * math.sin(angle + math.pi / 6))
            self.draw.polygon([end_point, p1, p2], fill=color)
        except Exception as e:
            self.logger.warning(f"Could not draw arrowhead. {e}")
