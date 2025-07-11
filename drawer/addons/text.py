# drawer/addons/text.py
import math
from PIL import Image, ImageDraw
from .base import Base
from ..models.node import TextObject

class Text(Base):
    """Draws all text elements, including labels for nodes and edges."""
    def run(self):
        # Draw labels for all drawable objects (nodes and edges)
        for obj in self.renderer.drawable_objects:
            label_text, label_pos_name = obj.get_label_text_and_position()
            if not label_text: continue

            if obj.__class__.__name__ == 'EdgeObject':
                self._draw_edge_label(obj, label_text)
            else: # For NodeObjects
                self._draw_node_label(obj, label_text, label_pos_name)
        
        # Draw standalone text nodes
        for node in self.renderer.nodes:
            if isinstance(node, TextObject):
                self.draw.text(node.position, node.text, fill=node.color, font=self.renderer.font)

    def _draw_node_label(self, node, text, position):
        """Draws a label for a given node (icon or shape)."""
        self.logger.debug(f"Drawing label for node '{node.id}' at position '{position}'")
        label_pos, text_anchor = self._get_label_position_and_anchor(node.position, node.bbox, position)
        self.draw.text(label_pos, text, fill="#000000", font=self.renderer.font, anchor=text_anchor)

    def _draw_edge_label(self, edge, text):
        """Draws a rotated label with a background along an edge."""
        start_pos, end_pos = self.renderer.get_edge_endpoints(edge)
        if not start_pos or not end_pos: return

        self.logger.debug(f"Drawing label for edge '{edge.id}'")

        # Calculate angle and midpoint of the edge
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        angle = math.degrees(math.atan2(dy, dx))
        mid_point = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2)

        # --- New: Smart text rotation ---
        # If the angle is upside down (e.g., for right-to-left lines), flip it
        if 90 < abs(angle) < 270:
            angle -= 180

        # Create a temporary image for the text
        text_bbox = self.renderer.font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Add padding for the background
        padding = 5 * self.scale_factor
        bg_width = text_width + (2 * padding)
        bg_height = text_height + (2 * padding)

        txt_img = Image.new('RGBA', (bg_width, bg_height))
        txt_draw = ImageDraw.Draw(txt_img)

        # --- New: Draw background rectangle ---
        canvas_bg_color = self.renderer.canvas_config.get('background_color', 'white')
        txt_draw.rectangle([0, 0, bg_width, bg_height], fill=canvas_bg_color)
        
        # Draw the text onto its temporary image
        txt_draw.text((padding, padding), text, font=self.renderer.font, fill=edge.color)

        # Rotate the text image and paste it onto the main canvas
        rotated_txt = txt_img.rotate(angle, expand=1, resample=Image.BICUBIC)
        
        # Calculate paste position to center the rotated text on the midpoint
        paste_x = int(mid_point[0] - rotated_txt.width / 2)
        paste_y = int(mid_point[1] - rotated_txt.height / 2)
        
        self.image.paste(rotated_txt, (paste_x, paste_y), rotated_txt)

    def _get_label_position_and_anchor(self, obj_pos, obj_bbox, label_pos_name):
        x, y = obj_pos; w, h = obj_bbox
        offset = 5 * self.scale_factor
        pos_map = {
            'top': ((x + w / 2, y - offset), "mb"), 'bottom': ((x + w / 2, y + h + offset), "mt"),
            'left': ((x - offset, y + h / 2), "rm"), 'right': ((x + w + offset, y + h / 2), "lm"),
            'center': ((x + w / 2, y + h / 2), "mm"), 'top_left': ((x, y), "lb"),
            'top_right': ((x + w, y), "rb"), 'bottom_left': ((x, y + h), "lt"),
            'bottom_right': ((x + w, y + h), "rt")
        }
        return pos_map.get(label_pos_name, pos_map['bottom'])
