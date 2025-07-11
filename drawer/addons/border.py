# drawer/addons/border.py
from .base import Base
from .utils import draw_dashed_path

class Border(Base):
    """Draws a border around the canvas if specified in the config."""
    def run(self):
        border_config = self.config.get('canvas', {}).get('border')
        if not border_config:
            self.logger.debug("No border configuration found. Skipping.")
            return

        color = border_config.get('color', 'black')
        width = border_config.get('width', 1) * self.scale_factor
        border_type = border_config.get('type', 'solid')
        
        self.logger.debug(f"Drawing canvas border: type='{border_type}', width={width}, color='{color}'")

        w, h = self.image.width, self.image.height
        points = [(0, 0), (w - 1, 0), (w - 1, h - 1), (0, h - 1), (0, 0)]
        
        if border_type == 'solid':
            self.draw.line(points, fill=color, width=width)
        else:
            dash_length = 10 * self.scale_factor if border_type == 'dashed' else 2 * self.scale_factor
            draw_dashed_path(self.draw, points, color, width, dash_length)
        
        self.logger.debug("Canvas border drawing complete.")
