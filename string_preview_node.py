class StringPreviewNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_string",)
    FUNCTION = "preview_string"
    CATEGORY = "utils/StringEssentials"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Force re-evaluation every time to ensure fresh data in PNG metadata
        return float("nan")

    def preview_string(self, input_string=""):
        return {"ui": {"text": (input_string,)}, "result": (input_string,)}