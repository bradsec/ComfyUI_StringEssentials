class StringContainsAnyNode:
    """Check if an input string contains any of multiple substrings."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {
                    "forceInput": True,
                    "tooltip": "The string to search within"
                }),
                "substrings": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Enter substrings to search for (one per line)",
                    "tooltip": "Enter substrings to check (one per line). Returns true if ANY are found."
                }),
                "match_case": ("BOOLEAN", {
                    "default": False,
                    "label_on": "enabled",
                    "label_off": "disabled",
                    "tooltip": "Whether the search should be case-sensitive"
                })
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING")
    RETURN_NAMES = ("contains_any", "matched_string")
    FUNCTION = "contains_any"
    CATEGORY = "utils/StringEssentials"

    def contains_any(self, input_string, substrings, match_case):
        # Parse substrings, one per line
        substrings_list = []
        for line in substrings.splitlines():
            line = line.strip()
            if line:
                substrings_list.append(line)

        if not substrings_list:
            return (False, "")

        # Prepare strings for comparison
        search_string = input_string if match_case else input_string.lower()

        # Check each substring
        for substring in substrings_list:
            check_substring = substring if match_case else substring.lower()
            if check_substring in search_string:
                return (True, substring)

        return (False, "")
