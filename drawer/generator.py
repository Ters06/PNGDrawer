# drawer/generator.py
import math
import io
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from .config import OUTPUT_DIR, ICONS_DIR
from .addons.shape import Shape
from .addons.edge import Edge
from .addons.icon import Icon
from .addons.text import Text

class ImageRenderer:
    """Renders an image by orchestrating a series of drawing addons."""

    def __init__(self, config: dict):
        self.config = config
        self.canvas_config = config.get('canvas', {})
        self.nodes = config.get('nodes', [])
        self.icons_map = config.get('icons', {})
        self.final_positions = {}
        self.object_bboxes = {}
        self.loaded_images = {}
        self.scale_factor = 4
        
        try:
            font_path_bytes = subprocess.check_output(["fc-match", "--format=%{file}", "dejavusans"])
            font_path = font_path_bytes.decode().strip()
            self.font = ImageFont.truetype(font_path, 15 * self.scale_factor)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.font = ImageFont.load_default()

    def render(self):
        """The main method to orchestrate the image rendering."""
        final_width = self.canvas_config.get('width', 1200)
        final_height = self.canvas_config.get('height', 600)
        upscaled_width = final_width * self.scale_factor
        upscaled_height = final_height * self.scale_factor
        bg_color = self.canvas_config.get('background_color', 'white')
        
        self.image = Image.new('RGBA', (upscaled_width, upscaled_height), color=bg_color)
        self.draw = ImageDraw.Draw(self.image)
        
        self._prepare_all_objects()
        self._resolve_all_positions()
        
        # --- Run addons in a specific order ---
        addons = [
            Shape(self),
            Edge(self),
            Icon(self),
            Text(self)
        ]
        for addon in addons:
            addon.run()

        self.image = self.image.resize((final_width, final_height), Image.Resampling.LANCZOS)

        main_config = self.config.get('main', {})
        output_filename = main_config.get('output_filename', 'diagram')
        png_filename = Path(output_filename).with_suffix('.png')
        output_filepath = OUTPUT_DIR / png_filename
        
        self.image.save(output_filepath, 'PNG')
        print(f"✅ Image successfully rendered at: {output_filepath}")

    def _prepare_all_objects(self):
        """Pre-calculates bounding boxes and resizes/loads images for all nodes."""
        for node_config in self.nodes:
            node_id = node_config['id']
            bbox = (0, 0)
            node_type = node_config.get('type')

            if node_type == 'text':
                bbox = self.draw.textbbox((0,0), node_config.get('text', ''), font=self.font)[2:]
            elif node_type == 'shape':
                bbox = tuple(dim * self.scale_factor for dim in node_config.get('size', [50, 50]))
            elif node_type == 'icon':
                icon_img = self._load_and_resize_icon(node_config)
                if icon_img:
                    self.loaded_images[node_id] = icon_img
                    bbox = icon_img.size
                else:
                    bbox = tuple(dim * self.scale_factor for dim in node_config.get('size', [64, 64]))
            self.object_bboxes[node_id] = bbox

    def _load_and_resize_icon(self, node_config):
        icon_id = node_config.get('icon_id'); icon_path_str = self.icons_map.get(icon_id)
        if not icon_id or not icon_path_str: return None
        icon_path = ICONS_DIR / icon_path_str
        if not icon_path.is_file(): return None
        target_size = tuple(dim * self.scale_factor for dim in node_config.get('size', [64,64]))
        if icon_path.suffix.lower() == '.svg':
            png_data = cairosvg.svg2png(url=str(icon_path), output_width=target_size[0], output_height=target_size[1])
            return Image.open(io.BytesIO(png_data))
        else:
            img = Image.open(icon_path)
            return img.resize(target_size, Image.Resampling.LANCZOS)

    def _resolve_all_positions(self):
        for _ in range(len(self.nodes) + 1):
            for node in self.nodes:
                if node['id'] in self.final_positions: continue
                pos = self._calculate_single_position(node)
                if pos is not None: self.final_positions[node['id']] = pos

    def _calculate_single_position(self, node):
        placement = node.get('placement', {}); bbox = self.object_bboxes.get(node['id'], (0,0))
        if placement.get('type') == 'absolute':
            return (placement.get('x', 0) * self.scale_factor, placement.get('y', 0) * self.scale_factor)
        if placement.get('type') == 'relative':
            target_id = placement.get('target_id')
            if target_id not in self.final_positions: return None
            target_pos = self.final_positions[target_id]; target_bbox = self.object_bboxes[target_id]
            target_anchor = self.get_anchor_point(target_pos, target_bbox, placement.get('target_anchor'))
            self_anchor = self.get_anchor_point((0,0), bbox, placement.get('self_anchor'))
            offset_x = placement.get('offset', {}).get('x', 0) * self.scale_factor
            offset_y = placement.get('offset', {}).get('y', 0) * self.scale_factor
            return (int(target_anchor[0] - self_anchor[0] + offset_x), int(target_anchor[1] - self_anchor[1] + offset_y))
        return (0, 0)

    def get_anchor_point(self, pos_xy, bbox, anchor_name):
        x, y = pos_xy; width, height = bbox
        if anchor_name == 'center': return (x + width / 2, y + height / 2)
        if anchor_name == 'left': return (x, y + height / 2)
        if anchor_name == 'right': return (x + width, y + height / 2)
        if anchor_name == 'top': return (x + width / 2, y)
        if anchor_name == 'bottom': return (x + width / 2, y + height)
        return pos_xy

    def get_edge_endpoints(self, edge):
        source_pos = self.final_positions.get(edge['source_id'])
        target_pos = self.final_positions.get(edge['target_id'])
        if not source_pos or not target_pos: return None, None
        source_bbox = self.object_bboxes[edge['source_id']]
        target_bbox = self.object_bboxes[edge['target_id']]
        start = self.get_anchor_point(source_pos, source_bbox, edge.get('source_anchor', 'right'))
        end = self.get_anchor_point(target_pos, target_bbox, edge.get('target_anchor', 'left'))
        return start, end
