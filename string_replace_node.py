import re

class StringReplaceNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "replacement_pairs": ("STRING", {"multiline": True, "default": "",
                    "tooltip": "Enter replacement pairs, one per line, in format 'search:replace'. Example: 'cat:dog' or 'A drawing of:A photo of'"}),
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
    FUNCTION = "string_replace"
    CATEGORY = "utils"

    def string_replace(self, input_string, replacement_pairs, match_case, match_whole_string, remove_extra_spaces):
        result = input_string
        flags = 0 if match_case else re.IGNORECASE

        for line in replacement_pairs.splitlines():
            line = line.strip()
            if not line or ':' not in line:
                continue

            search_str, replace_str = line.split(':', 1)
            search_str = search_str.strip()
            replace_str = replace_str.strip()

            if not search_str:
                continue

            if match_whole_string:
                pattern = re.escape(search_str)
                pattern = r"(?<!\S)" + pattern + r"(?!\S)"
            else:
                pattern = re.escape(search_str)

            result = re.sub(pattern, replace_str, result, flags=flags)

        if remove_extra_spaces:
            # Replace multiple spaces with single space
            result = re.sub(r'\s+', ' ', result)
        
        # Strip leading and trailing spaces
        result = result.strip()
        return (result,)