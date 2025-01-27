class StringTextboxNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {
                    "multiline": True, 
                    "default": "",
                    "tooltip": "Enter text here"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_string",)
    FUNCTION = "pass_string"
    CATEGORY = "utils"

    def pass_string(self, input_string):
        return (input_string,)