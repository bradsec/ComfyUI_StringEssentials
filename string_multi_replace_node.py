import re

class StringMultiReplaceNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "replacement_pairs": ("STRING", {"multiline": True, "default": "",
                    "tooltip": "Enter replacement pairs, one per line. Format: 'search<delimiter>replace'. Default delimiter is ':' (colon)"}),
                "replacement_delimiter": ("STRING", {"default": "::", 
                    "tooltip": "Character(s) that separate search and replace strings. Default is two '::' (colons)"}),
                "match_case": ("BOOLEAN", {"default": False,
                    "label_on": "enabled", "label_off": "disabled"}),
                "match_whole_string": ("BOOLEAN", {"default": False,
                    "label_on": "enabled", "label_off": "disabled"}),
                "remove_extra_spaces": ("BOOLEAN", {"default": True,
                    "label_on": "enabled", "label_off": "disabled"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("modified_string",)
    FUNCTION = "string_replace"
    CATEGORY = "utils"

    def cleanup_text(self, text):
        text = re.sub(r'\s+([,;:.])', r'\1', text)  # Remove spaces before punctuation
        text = re.sub(r'\s{2,}', ' ', text)  # Normalize multiple spaces
        return text.strip()

    def string_replace(self, input_string, replacement_pairs, replacement_delimiter, match_case, match_whole_string, remove_extra_spaces):
        # Create a list of all replacements
        replacements = []
        for line in replacement_pairs.splitlines():
            line = line.strip()
            if not line or replacement_delimiter not in line:
                continue

            search_str, replace_str = line.split(replacement_delimiter, 1)
            search_str = search_str.strip()
            replace_str = replace_str.strip()

            if not search_str:
                continue
                
            replacements.append((len(search_str), search_str, replace_str))
        
        # Sort by length in descending order
        replacements.sort(reverse=True)
        
        result = input_string
        flags = 0 if match_case else re.IGNORECASE

        # Perform replacements
        for _, search_str, replace_str in replacements:
            if match_whole_string:
                # Enhanced pattern to handle punctuation properly
                pattern = r'(?:\b|(?<=\s)|^)' + re.escape(search_str) + r'(?:[,;:.])?(?=\s|$)'
            else:
                # For non-whole string matching, still handle punctuation
                pattern = re.escape(search_str) + r'(?:[,;:.])?'
            
            regex = re.compile(pattern, flags=flags)
            result = regex.sub(replace_str, result)

        if remove_extra_spaces:
            result = self.cleanup_text(result)
            
        return (result,)
