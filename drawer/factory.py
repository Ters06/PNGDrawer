# drawer/factory.py
import sys
import importlib
from diagrams import Node # Import the generic Node

class NodeFactory:
    """Creates diagram node objects based on a type string from the JSON."""
    
    def get_node_class(self, type_string: str):
        """Dynamically imports the class for a node from the 'diagrams' library."""
        full_class_string = f"diagrams.{type_string}"
        try:
            module_path, class_name = full_class_string.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except (ImportError, AttributeError, ValueError):
            print(f"❌ Error: Could not find class for type '{type_string}'.")
            print("Please verify the type string in your JSON file matches the library's documentation.")
            sys.exit(1)

    def create_node(self, config: dict):
        """Creates an instance of a diagram node from its config."""
        node_type = config['type']
        
        # Handle our special text type
        if node_type == "util.text":
            # Use a generic Node and set Graphviz attributes for a clean text look
            return Node(
                label=config.get('label', ''),
                shape='plaintext' # This is the key attribute for text-only nodes
            )

        # Handle all other standard types
        node_class = self.get_node_class(node_type)
        return node_class(label=config.get('label', ''))
