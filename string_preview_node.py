class StringPreviewNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_string",)
    FUNCTION = "preview_string"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def preview_string(self, input_string=""):
        return {"ui": {"text": (input_string,)}, "result": (input_string,)}