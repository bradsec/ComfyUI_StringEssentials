"""String manipulation nodes for ComfyUI"""

from .string_textbox_node import StringTextboxNode
from .string_strip_node import StringStripNode
from .string_multi_replace_node import StringMultiReplaceNode 
from .string_preview_node import StringPreviewNode

NODE_CLASS_MAPPINGS = {
    "StringTextbox": StringTextboxNode,
    "StringStrip": StringStripNode,
    "StringMultiReplace": StringMultiReplaceNode,
    "StringPreview": StringPreviewNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringTextbox": "String Textbox",
    "StringStrip": "String Strip",
    "StringMultiReplace": "String Multi Replace",
    "StringPreview": "String Preview"
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
