import re

class StringConditionalAppendNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "strings_to_check": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Enter strings to check (one per line)",
                    "tooltip": "Enter strings to search for and append if not found (one per line)"
                }),
                "position": (["end", "beginning"], {
                    "default": "end",
                    "tooltip": "Where to add strings if not found"
                }),
                "match_case": ("BOOLEAN", {
                    "default": False,
                    "label_on": "enabled",
                    "label_off": "disabled",
                    "tooltip": "Whether the search should be case-sensitive"
                }),
                "separator": ("STRING", {
                    "default": ", ",
                    "tooltip": "Character(s) to use between text and appended strings"
                })
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("output_string", "was_appended")
    FUNCTION = "conditional_append"
    CATEGORY = "utils/StringEssentials"

    def conditional_append(self, input_string, strings_to_check, position, match_case, separator):
        # Parse strings to check, one per line
        strings_list = []
        for line in strings_to_check.splitlines():
            line = line.strip()
            if line:
                strings_list.append(line)

        if not strings_list:
            return (input_string, False)

        result = input_string
        was_any_appended = False

        # Check and append each string if not found
        for check_string in strings_list:
            # Check if check_string exists in current result
            if match_case:
                string_found = check_string in result
            else:
                string_found = check_string.lower() in result.lower()

            # If string not found, append it
            if not string_found:
                if position == "beginning":
                    result = check_string + separator + result
                else:  # end
                    result = result + separator + check_string
                was_any_appended = True

        return (result, was_any_appended)
