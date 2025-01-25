"""String manipulation nodes for ComfyUI"""

from .string_strip_node import StringStripNode
from .string_replace_node import StringReplaceNode

NODE_CLASS_MAPPINGS = {
    "StringStrip": StringStripNode,
    "StringReplace": StringReplaceNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringStrip": "String Strip",
    "StringReplace": "String Replace"
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]