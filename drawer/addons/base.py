# drawer/addons/base.py

class Base:
    """A base class for all drawing addons."""
    def __init__(self, renderer):
        self.renderer = renderer
        self.config = renderer.config
        self.image = renderer.image
        self.draw = renderer.draw
        self.scale_factor = renderer.scale_factor

    def run(self):
        """This method will be implemented by each specific addon."""
        raise NotImplementedError
