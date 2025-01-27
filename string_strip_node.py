import re

class StringStripNode:
    @classmethod
    def INPUT_TYPES(cls):
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

    def cleanup_text(self, text):
        text = re.sub(r'\s+([,;:.])', r'\1', text)  # Remove spaces before punctuation
        text = re.sub(r'\s{2,}', ' ', text)  # Normalize multiple spaces
        return text.strip()

    def string_strip(self, input_string, strings_to_remove, match_case, match_whole_string, remove_extra_spaces):
        # Create a list of strings to remove, sorted by length
        removals = []
        for line in strings_to_remove.splitlines():
            line = line.strip()
            if not line:
                continue
            
            # Store length with the string for sorting
            removals.append((len(line), line))
        
        # Sort by length in descending order to handle longer phrases first
        removals.sort(reverse=True)
        
        result = input_string
        flags = 0 if match_case else re.IGNORECASE

        # Compile patterns once for better performance
        patterns = []
        for _, string_to_remove in removals:
            if match_whole_string:
                # Enhanced pattern to handle punctuation properly
                # Look for the string followed by optional punctuation
                pattern = r'(?:\b|(?<=\s)|^)' + re.escape(string_to_remove) + r'(?:[,;:.])?(?=\s|$)'
            else:
                # For non-whole string matching, still handle punctuation
                pattern = re.escape(string_to_remove) + r'(?:[,;:.])?'
            
            patterns.append(re.compile(pattern, flags=flags))

        # Apply all removal patterns
        for pattern in patterns:
            result = pattern.sub('', result)

        if remove_extra_spaces:
            result = self.cleanup_text(result)
        
        return (result,)