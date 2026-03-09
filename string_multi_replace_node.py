import re

class StringMultiReplaceNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {
                    "forceInput": True,
                    "tooltip": "The string to process"
                }),
                "replacement_pairs": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter replacement pairs (one per line)",
                    "tooltip": "Enter replacement pairs (one per line). Format: 'search<delimiter>replace'. Default delimiter is ':' (colon)"}),
                "replacement_delimiter": ("STRING", {"default": "::",
                    "tooltip": "Character(s) that separate search and replace strings. Default is two '::' (colons)"}),
                "match_case": ("BOOLEAN", {"default": False,
                    "label_on": "enabled", "label_off": "disabled"}),
                "match_whole_string": ("BOOLEAN", {"default": False,
                    "label_on": "enabled", "label_off": "disabled"}),
                "preserve_punctuation": ("BOOLEAN", {"default": True,
                    "label_on": "enabled", "label_off": "disabled",
                    "tooltip": "When enabled, punctuation marks adjacent to matched text are preserved"}),
                "remove_extra_spaces": ("BOOLEAN", {"default": True,
                    "label_on": "enabled", "label_off": "disabled"}),
                "sort_by_length": ("BOOLEAN", {"default": True,
                    "label_on": "enabled", "label_off": "disabled",
                    "tooltip": "When enabled, longer search strings are replaced first to prevent substring clobbering. Disable for input-order replacement."}),
                "use_regex": ("BOOLEAN", {"default": False,
                    "label_on": "enabled", "label_off": "disabled",
                    "tooltip": "When enabled, search strings are treated as regex patterns instead of literal text"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("modified_string",)
    FUNCTION = "string_replace"
    CATEGORY = "utils/StringEssentials"

    def cleanup_text(self, text):
        text = re.sub(r'\s+([,;:.])', r'\1', text)  # Remove spaces before punctuation
        text = re.sub(r'\s{2,}', ' ', text)  # Normalize multiple spaces
        return text.strip()

    def string_replace(self, input_string, replacement_pairs, replacement_delimiter, match_case, match_whole_string, preserve_punctuation, remove_extra_spaces, sort_by_length=True, use_regex=False):
        # Create a list of all replacements
        replacements = []
        for line in replacement_pairs.splitlines():
            # Don't strip the line yet to preserve trailing whitespace in replacements (Issue #8)
            if not line or line.isspace() or replacement_delimiter not in line:
                continue

            search_str, replace_str = line.split(replacement_delimiter, 1)
            search_str = search_str.strip()
            # Don't strip replace_str to allow intentional spaces/whitespace (Issue #8)

            if not search_str:
                continue

            replacements.append((len(search_str), search_str, replace_str))

        # Sort by length in descending order (longest first to prevent substring clobbering)
        if sort_by_length:
            replacements.sort(reverse=True)

        result = input_string
        flags = 0 if match_case else re.IGNORECASE

        # Perform replacements
        for _, search_str, replace_str in replacements:
            escaped = search_str if use_regex else re.escape(search_str)
            if match_whole_string:
                if preserve_punctuation:
                    # Match whole words but preserve adjacent punctuation
                    pattern = r'\b' + escaped + r'\b'
                else:
                    # Original behavior: remove punctuation after match
                    pattern = r'(?:\b|(?<=\s)|^)' + escaped + r'(?:[,;:.])?(?=\s|$)'
            else:
                if preserve_punctuation:
                    # Simple replacement preserving punctuation
                    pattern = escaped
                else:
                    # Original behavior: remove punctuation after match
                    pattern = escaped + r'(?:[,;:.])?'

            regex = re.compile(pattern, flags=flags)
            result = regex.sub(replace_str, result)

        if remove_extra_spaces:
            result = self.cleanup_text(result)

        return (result,)
