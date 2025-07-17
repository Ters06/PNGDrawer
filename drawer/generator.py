# drawer/generator.py
import math
import io
import subprocess
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from .config import OUTPUT_DIR, ICONS_DIR
from .models.node import IconObject, NodeObject, ShapeObject, TextObject
from .models.edge import EdgeObject
from .addons.shape import Shape
from .addons.edge import Edge
from .addons.icon import Icon
from .addons.text import Text
from .addons.border import Border

class ImageRenderer:
    """Renders an image by orchestrating a series of drawing addons."""

    def __init__(self, config: dict):
        self.config = config
        self.main_config = config.get('main', {})
        self.canvas_config = config.get('canvas', {})
        self.icons_map = config.get('icons', {})
        self.scale_factor = 4
        self.logger = logging.getLogger(__name__)
        
        self.nodes = [self._create_node_obj(n) for n in config.get('nodes', [])]
        self.edges = [EdgeObject(e) for e in config.get('edges', [])]
        self.drawable_objects = self.nodes + self.edges
        
        try:
            # Use the new default_font_size from main.json, fallback to 15
            default_font_size = self.main_config.get('default_font_size', 15)
            font_path_bytes = subprocess.check_output(["fc-match", "--format=%{file}", "dejavusans"])
            font_path = font_path_bytes.decode().strip()
            self.font = ImageFont.truetype(font_path, default_font_size * self.scale_factor)
            self.logger.info(f"Successfully loaded font: {font_path}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("Could not find font 'dejavusans' via fc-match. Falling back to default.")
            self.font = ImageFont.load_default()

    def _create_node_obj(self, config):
        """Factory function to create the correct NodeObject subclass."""
        node_type = config.get('type')
        if node_type == 'icon': return IconObject(config)
        if node_type == 'shape': return ShapeObject(config)
        if node_type == 'text': return TextObject(config)
        self.logger.warning(f"Unknown node type '{node_type}'. Using generic NodeObject.")
        return NodeObject(config)

    def render(self):
        """The main method to orchestrate the image rendering."""
        self.logger.info("--- Starting Diagram Rendering ---")
        final_width = self.canvas_config.get('width', 1200)
        final_height = self.canvas_config.get('height', 600)
        
        upscaled_width = final_width * self.scale_factor
        upscaled_height = final_height * self.scale_factor
        bg_color = self.canvas_config.get('background_color', 'white')
        
        self.image = Image.new('RGBA', (upscaled_width, upscaled_height), color=bg_color)
        self.draw = ImageDraw.Draw(self.image)
        
        self._prepare_all_objects()
        self._resolve_all_positions()
        
        addons = [
            ("ShapeAddon", Shape(self)),
            ("EdgeAddon", Edge(self)),
            ("IconAddon", Icon(self)),
            ("TextAddon", Text(self)),
            ("BorderAddon", Border(self))
        ]
        self.logger.info("Step 3: Running drawing addons...")
        for name, addon in addons:
            self.logger.debug(f"Running addon: {name}")
            addon.run()
        
        self.logger.info("Step 4: Downscaling final image for anti-aliasing...")
        self.image = self.image.resize((final_width, final_height), Image.Resampling.LANCZOS)

        output_filename = self.main_config.get('output_filename', 'diagram')
        png_filename = Path(output_filename).with_suffix('.png')
        output_filepath = OUTPUT_DIR / png_filename
        
        self.image.save(output_filepath, 'PNG')
        self.logger.info(f"--- Diagram Rendering Complete ---")
        print(f"✅ Image successfully rendered at: {output_filepath}")

    def _prepare_all_objects(self):
        self.logger.info("Step 1: Preparing all objects (calculating sizes)...")
        for obj in self.nodes:
            bbox = (0, 0)
            if isinstance(obj, TextObject):
                bbox = self.draw.textbbox((0,0), obj.text, font=self.font)[2:]
            elif isinstance(obj, ShapeObject):
                bbox = tuple(dim * self.scale_factor for dim in obj.size)
            elif isinstance(obj, IconObject):
                icon_img = self._load_and_resize_icon(obj)
                if icon_img:
                    obj.loaded_image = icon_img
                    bbox = icon_img.size
                else:
                    bbox = tuple(dim * self.scale_factor for dim in obj.size)
            obj.bbox = bbox
            self.logger.debug(f"  > Prepared node '{obj.id}': BBox={bbox}")

    def _load_and_resize_icon(self, icon_obj):
        icon_path_str = self.icons_map.get(icon_obj.icon_id)
        if not icon_path_str: 
            self.logger.warning(f"Icon ID '{icon_obj.icon_id}' not found in icons.json.")
            return None
        icon_path = ICONS_DIR / icon_path_str
        if not icon_path.is_file():
            self.logger.error(f"Icon file NOT FOUND at path: {icon_path}")
            return None
        
        target_size = tuple(dim * self.scale_factor for dim in icon_obj.size)
        if icon_path.suffix.lower() == '.svg':
            png_data = cairosvg.svg2png(url=str(icon_path), output_width=target_size[0], output_height=target_size[1])
            return Image.open(io.BytesIO(png_data))
        else:
            img = Image.open(icon_path)
            return img.resize(target_size, Image.Resampling.LANCZOS)

    def _resolve_all_positions(self):
        self.logger.info("Step 2: Resolving all object positions...")
        max_passes = len(self.nodes) + 1
        for i in range(max_passes):
            unresolved_nodes = [n for n in self.nodes if not hasattr(n, 'resolved_position')]
            if not unresolved_nodes:
                self.logger.info("All node positions resolved.")
                return
            for node in unresolved_nodes:
                pos = self._calculate_single_position(node)
                if pos is not None:
                    node.position = pos
                    node.resolved_position = True
        if unresolved_nodes:
            self.logger.error(f"Could not resolve positions for all nodes. Unresolved: {[n.id for n in unresolved_nodes]}")

    def _calculate_single_position(self, node):
        placement = node.placement
        if placement.get('type') == 'absolute':
            return (placement.get('x', 0) * self.scale_factor, placement.get('y', 0) * self.scale_factor)
        if placement.get('type') == 'relative':
            target_obj = self.get_object_by_id(placement.get('target_id'))
            if not target_obj or not hasattr(target_obj, 'resolved_position'): return None
            
            target_anchor = self.get_anchor_point(target_obj.position, target_obj.bbox, placement.get('target_anchor'))
            self_anchor = self.get_anchor_point((0,0), node.bbox, placement.get('self_anchor'))
            offset_x = placement.get('offset', {}).get('x', 0) * self.scale_factor
            offset_y = placement.get('offset', {}).get('y', 0) * self.scale_factor
            return (int(target_anchor[0] - self_anchor[0] + offset_x), int(target_anchor[1] - self_anchor[1] + offset_y))
        return (0, 0)
    
    def get_object_by_id(self, obj_id):
        for obj in self.drawable_objects:
            if obj.id == obj_id:
                return obj
        self.logger.warning(f"Could not find object with ID: '{obj_id}'")
        return None

    def get_anchor_point(self, pos_xy, bbox, anchor_name):
        """Calculates the coordinates of a specific anchor point on an object."""
        x, y = pos_xy
        w, h = bbox

        # Horizontal alignment
        if 'left' in anchor_name:
            x_coord = x
        elif 'right' in anchor_name:
            x_coord = x + w
        else: # center, top, bottom
            x_coord = x + w / 2

        # Vertical alignment
        if 'top' in anchor_name:
            y_coord = y
        elif 'bottom' in anchor_name:
            y_coord = y + h
        else: # center, left, right
            y_coord = y + h / 2
            
        return (x_coord, y_coord)

    def get_edge_endpoints(self, edge):
        source_obj = self.get_object_by_id(edge.source_id)
        target_obj = self.get_object_by_id(edge.target_id)
        if not source_obj or not target_obj: return None, None
        start = self.get_anchor_point(source_obj.position, source_obj.bbox, edge.source_anchor)
        end = self.get_anchor_point(target_obj.position, target_obj.bbox, edge.target_anchor)
        return start, end
