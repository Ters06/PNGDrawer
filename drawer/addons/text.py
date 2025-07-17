# drawer/addons/text.py
import math
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
from .base import Base
from ..models.node import TextObject, ShapeObject, IconObject

class Text(Base):
    """Draws all text elements, including labels for nodes and edges."""

    def _get_font(self, label_config, default_font):
        """
        Gets the correct font based on label styling by querying the system's font cache.
        Falls back to the default font if a specific style cannot be found.
        """
        default_font_size = self.renderer.main_config.get('default_font_size', 12)
        
        font_family = label_config.get("font_family", "dejavusans")
        font_size = label_config.get("font_size", default_font_size)
        font_weight = label_config.get("font_weight")
        font_style = label_config.get("font_style")

        pattern = font_family
        if font_weight == "bold":
            pattern += ":weight=bold"
        if font_style == "italic":
            pattern += ":style=italic"

        try:
            font_path_bytes = subprocess.check_output(["fc-match", "--format=%{file}", pattern])
            font_path = font_path_bytes.decode().strip()
            return ImageFont.truetype(font_path, font_size * self.scale_factor)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning(f"Could not find a font matching '{pattern}'. Falling back to default.")
            return default_font

    def _wrap_text(self, text, width, font, draw):
        """Wraps text to fit within a given width."""
        lines = []
        words = text.split()
        
        if not words:
            return ""

        current_line = words[0]
        for word in words[1:]:
            if draw.textlength(word, font=font) > width:
                lines.append(current_line)
                lines.append(word)
                current_line = ""
                continue

            if draw.textlength(current_line + " " + word, font=font) <= width:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)

    def run(self):
        for obj in self.renderer.drawable_objects:
            label_data = obj.label
            label_config = None

            # Handle both simple string and object formats for labels
            if isinstance(label_data, str):
                # Convert simple string to a config object with default position
                label_config = {"text": label_data, "position": "bottom"}
            elif isinstance(label_data, dict):
                label_config = label_data
            else:
                # If label is None or not a supported type, skip
                continue

            label_text = label_config.get("text")
            if not label_text:
                continue

            if obj.__class__.__name__ == 'EdgeObject':
                self._draw_edge_label(obj, label_text)
            else:
                self._draw_node_label(obj, label_config)
        
        for node in self.renderer.nodes:
            if isinstance(node, TextObject):
                self.draw.text(node.position, node.text, fill=node.color, font=self.renderer.font)

    def _draw_node_label(self, node, label_config):
        """Draws a label for a given node, with styling, wrapping, and alignment."""
        text = label_config.get("text")
        position = label_config.get("position", "center")
        self.logger.debug(f"Drawing label for node '{node.id}' at position '{position}'")

        font = self._get_font(label_config, self.renderer.font)
        fill_color = label_config.get("color", "#000000")
        text_align = label_config.get("text_align", "center")

        text_to_draw = text
        padding = 15 * self.scale_factor
        if label_config.get("wrapping") == "auto" and position == "center":
            max_width = node.bbox[0] - (2 * padding)
            text_to_draw = self._wrap_text(text, max_width, font, self.draw)
        
        if position == "center":
            bbox = self.draw.multiline_textbbox((0, 0), text_to_draw, font=font, align=text_align)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            y = node.position[1] + (node.bbox[1] - text_height) / 2

            if text_align == "left":
                x = node.position[0] + padding
            elif text_align == "right":
                x = node.position[0] + node.bbox[0] - text_width - padding
            else:
                x = node.position[0] + (node.bbox[0] - text_width) / 2
            
            self.draw.multiline_text((x, y), text_to_draw, fill=fill_color, font=font, align=text_align)
        else:
            label_pos, text_anchor = self._get_label_position_and_anchor(node.position, node.bbox, position)
            self.draw.text(label_pos, text_to_draw, fill=fill_color, font=font, anchor=text_anchor)

    def _draw_edge_label(self, edge, text):
        """Draws a rotated label with a background along an edge. (UNCHANGED)"""
        start_pos, end_pos = self.renderer.get_edge_endpoints(edge)
        if not start_pos or not end_pos: return

        self.logger.debug(f"Drawing label for edge '{edge.id}'")
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        angle = math.degrees(math.atan2(dy, dx))
        mid_point = ((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2)

        if 90 < abs(angle) < 270:
            angle -= 180

        text_bbox = self.renderer.font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        padding = 5 * self.scale_factor
        bg_width = int(text_width + (2 * padding))
        bg_height = int(text_height + (2 * padding))

        txt_img = Image.new('RGBA', (bg_width, bg_height))
        txt_draw = ImageDraw.Draw(txt_img)

        canvas_bg_color = self.renderer.canvas_config.get('background_color', 'white')
        txt_draw.rectangle([0, 0, bg_width, bg_height], fill=canvas_bg_color)
        
        txt_draw.text((padding, padding), text, font=self.renderer.font, fill=edge.color)

        rotated_txt = txt_img.rotate(angle, expand=1, resample=Image.BICUBIC)
        
        paste_x = int(mid_point[0] - rotated_txt.width / 2)
        paste_y = int(mid_point[1] - rotated_txt.height / 2)
        
        self.image.paste(rotated_txt, (paste_x, paste_y), rotated_txt)

    def _get_label_position_and_anchor(self, obj_pos, obj_bbox, label_pos_name):
        """(UNCHANGED)"""
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
