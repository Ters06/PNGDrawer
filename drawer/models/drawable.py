# drawer/models/drawable.py

class DrawableObject:
    """A base class for any object that can be drawn on the canvas."""
    def __init__(self, config):
        self.id = config.get('id')
        self.layer = config.get('layer', 1)
        self.placement = config.get('placement', {})
        self.label_config = config.get('label')
        
        # These will be calculated by the renderer
        self.position = (0, 0)
        self.bbox = (0, 0)

    def get_label_text_and_position(self):
        """Parses the label property and returns the text and position."""
        if not self.label_config:
            return None, None
        
        if isinstance(self.label_config, str):
            return self.label_config, "bottom" # Default position
        elif isinstance(self.label_config, dict):
            return self.label_config.get('text'), self.label_config.get('position', 'bottom')
        
        return None, None
