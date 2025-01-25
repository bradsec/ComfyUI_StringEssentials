import re

class StringStripNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "strings_to_remove": ("STRING", {"multiline": True, "default": "",
                    "tooltip": "Enter strings to remove, one per line. Can include multiple words or strings on one line like: 'This image is'. This will only match this entire string."}),
                "match_case": ("BOOLEAN", {"default": False,
                    "label_on": "enabled", "label_off": "disabled"}),
                "match_whole_string": ("BOOLEAN", {"default": True,
                    "label_on": "enabled", "label_off": "disabled"}),
                "remove_extra_spaces": ("BOOLEAN", {"default": True,
                    "label_on": "enabled", "label_off": "disabled"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("modified_string",)
    FUNCTION = "string_strip"
    CATEGORY = "utils"

    def string_strip(self, input_string, strings_to_remove, remove_extra_spaces, match_case, match_whole_string):
        result = input_string
        flags = 0 if match_case else re.IGNORECASE

        for string_to_remove in strings_to_remove.splitlines():
            string_to_remove = string_to_remove.strip()
            if not string_to_remove:
                continue

            if match_whole_string:
                pattern = re.escape(string_to_remove)
                pattern = r"(?<!\S)" + pattern + r"(?!\S)"
            else:
                pattern = re.escape(string_to_remove)

            result = re.sub(pattern, "", result, flags=flags)

        if remove_extra_spaces:
            # Replace multiple spaces with single space
            result = re.sub(r'\s+', ' ', result)
        
        # Strip leading and trailing spaces
        result = result.strip()
        return (result,)