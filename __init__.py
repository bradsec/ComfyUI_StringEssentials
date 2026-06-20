"""String manipulation nodes for ComfyUI"""

from .string_textbox_node import StringTextboxNode
from .string_strip_node import StringStripNode
from .string_multi_replace_node import StringMultiReplaceNode
from .string_preview_node import StringPreviewNode
from .string_conditional_append_node import StringConditionalAppendNode
from .string_contains_any_node import StringContainsAnyNode

NODE_CLASS_MAPPINGS = {
    "StringTextbox": StringTextboxNode,
    "StringStrip": StringStripNode,
    "StringMultiReplace": StringMultiReplaceNode,
    "StringPreview": StringPreviewNode,
    "StringConditionalAppend": StringConditionalAppendNode,
    "StringContainsAny": StringContainsAnyNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringTextbox": "String Textbox",
    "StringStrip": "String Strip",
    "StringMultiReplace": "String Multi Replace",
    "StringPreview": "String Preview",
    "StringConditionalAppend": "String Conditional Append",
    "StringContainsAny": "String Contains Any"
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

# V3 schema wrappers, exposed only when comfy_api is importable. On the 0.25.0
# loader the V1 NODE_CLASS_MAPPINGS above win and comfy_entrypoint is skipped,
# so the nodes are not registered twice.
try:
    from .v3_nodes import comfy_entrypoint  # noqa: F401
    __all__.append("comfy_entrypoint")
except ImportError:
    pass
