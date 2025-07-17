# drawer/models/edge.py
from .drawable import DrawableObject

class EdgeObject(DrawableObject):
    """Represents a connection between two nodes."""
    def __init__(self, config):
        # Edges don't have an 'id' in the JSON, so we create one for internal use
        config['id'] = f"{config.get('source_id')}-to-{config.get('target_id')}"
        super().__init__(config)
        
        self.source_id = config.get('source_id')
        self.target_id = config.get('target_id')
        self.color = config.get('color', 'black')
        self.source_anchor = config.get('source_anchor', 'right')
        self.target_anchor = config.get('target_anchor', 'left')
        self.connection_config = config.get('connection', {})
        self.label = config.get('label')
