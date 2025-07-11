# drawer/models/node.py
from .drawable import DrawableObject

class NodeObject(DrawableObject):
    """A base class for all node-like objects (icons, shapes, text)."""
    def __init__(self, config):
        super().__init__(config)
        self.type = config.get('type')

class IconObject(NodeObject):
    def __init__(self, config):
        super().__init__(config)
        self.icon_id = config.get('icon_id')
        self.size = config.get('size', [64, 64])

class ShapeObject(NodeObject):
    def __init__(self, config):
        super().__init__(config)
        self.shape = config.get('shape')
        self.size = config.get('size')
        self.color = config.get('color')
        self.radius = config.get('radius')
        self.border = config.get('border')

class TextObject(NodeObject):
    def __init__(self, config):
        super().__init__(config)
        self.text = config.get('text')
        self.font_size = config.get('font_size')
        self.color = config.get('color')
