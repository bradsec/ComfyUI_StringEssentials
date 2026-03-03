# Coding Conventions

**Analysis Date:** 2026-03-03

## Naming Patterns

**Files:**
- Node files: `string_<name>_node.py` (e.g., `string_strip_node.py`, `string_multi_replace_node.py`)
- Test file: `test_<module>.py` (e.g., `test_string_nodes.py`)
- Class names reflect file names in PascalCase (e.g., `StringStripNode` from `string_strip_node.py`)

**Classes:**
- Node classes: `String<FunctionName>Node` format (e.g., `StringStripNode`, `StringMultiReplaceNode`, `StringConditionalAppendNode`)
- All node classes follow ComfyUI convention with specific class methods and attributes

**Functions/Methods:**
- snake_case for method names (e.g., `string_strip`, `cleanup_text`, `conditional_append`, `contains_any`)
- Core execution method: `FUNCTION = "<method_name>"` points to the main processing method
- Helper methods: lower case with underscores (e.g., `cleanup_text`)

**Variables:**
- snake_case for local variables (e.g., `input_string`, `strings_to_remove`, `replacement_pairs`, `strings_list`)
- Boolean prefixes: `match_case`, `match_whole_string`, `preserve_punctuation`, `was_appended`, `was_any_appended`

**Constants:**
- UPPERCASE for class constants (e.g., `RETURN_TYPES`, `RETURN_NAMES`, `FUNCTION`, `CATEGORY`, `INPUT_TYPES`, `OUTPUT_NODE`)

## Code Style

**Formatting:**
- No detected formatter configuration (.prettierrc, black config, etc.)
- Standard Python conventions: 4-space indentation
- Line length varies, no strict limit enforced
- Blank lines used to separate logical sections within methods

**Linting:**
- No detected linting configuration (.pylintrc, .flake8, etc.)
- Code follows general PEP 8 style conventions
- Minimal deviation from standard Python conventions

**Class Structure Pattern:**
All node classes follow a consistent structure:
```python
class StringNodeName:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "parameter_name": ("TYPE", {"configuration": "dict"})
            }
        }

    RETURN_TYPES = ("STRING",)  # or ("BOOLEAN", "STRING") etc.
    RETURN_NAMES = ("return_name",)
    FUNCTION = "method_name"
    CATEGORY = "utils/StringEssentials"

    def method_name(self, parameters):
        # Implementation
        return (result,)  # Always return tuple
```

## Import Organization

**Order:**
1. Standard library imports (`import unittest`, `import re`)
2. Class imports from local modules (e.g., `from string_strip_node import StringStripNode`)

**Path Aliases:**
- No path aliases detected or used

**Module Organization:**
- `__init__.py` at `/home/mark/Code/ComfyUI_StringEssentials/__init__.py` imports all node classes
- NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS provide ComfyUI registry
- All modules use relative imports in `__init__.py`

## Error Handling

**Patterns:**
- Input validation through conditional checks (if not line: continue)
- Empty input handling: return default empty/false values (e.g., `return (False, "")`)
- No explicit try-catch blocks; relies on Python built-ins for error prevention
- String operations wrapped in safe calls (e.g., `.strip()`, `.split()`)
- All methods handle empty strings and whitespace gracefully

**Example from `string_contains_any_node.py`:**
```python
if not substrings_list:
    return (False, "")

# Prepare strings for comparison
search_string = input_string if match_case else input_string.lower()
```

## Logging

**Framework:** Not detected - no logging module used in codebase

**Console Output:**
- No console logging throughout production code
- Tests use unittest assertions for verification
- No debug output or print statements in production code

## Comments

**When to Comment:**
- Comments reference issue numbers for fixes (e.g., "# Issue #6 fix", "# Test Issue #6", "# Issue #8")
- Comments explain regex patterns and matching behavior (e.g., "Remove spaces before punctuation", "Normalize multiple spaces")
- Docstrings minimal; only used in `StringContainsAnyNode` with class-level docstring

**JSDoc/TSDoc:**
- Not applicable - Python codebase without type hints
- Class methods have minimal/no docstrings

## Function Design

**Size:**
- Small to medium functions (methods range 10-50 lines)
- Core logic methods typically 30-50 lines: `string_strip`, `string_replace`, `conditional_append`
- Helper methods compact: `cleanup_text` is 3 lines

**Parameters:**
- Input parameters correspond directly to INPUT_TYPES definitions
- Boolean flags for feature toggling common (e.g., `match_case`, `preserve_punctuation`)
- String inputs often use multiline format for flexibility

**Return Values:**
- Always return tuples, matching RETURN_TYPES specification
- Single return: `(result,)`
- Multiple returns: `(result, boolean_flag)`
- Empty returns use falsy values: `(False, "")` or `(input_string, False)`

## Module Design

**Exports:**
- `__init__.py` at `/home/mark/Code/ComfyUI_StringEssentials/__init__.py` exports all node classes
- NODE_CLASS_MAPPINGS dict maps string names to classes for ComfyUI registration
- NODE_DISPLAY_NAME_MAPPINGS provides UI-friendly names

**Barrel Files:**
- Yes, `__init__.py` acts as barrel file with explicit imports
- Each node class imported individually
- WEB_DIRECTORY constant exported for ComfyUI

**Shared Utilities:**
- `cleanup_text()` method duplicated in both `StringStripNode` and `StringMultiReplaceNode` (not DRY, but isolated to context)
- No separate utils module; all logic encapsulated in node classes

## Common Patterns

**Regex Pattern Compilation:**
Patterns compiled once in a loop for performance:
```python
# From string_strip_node.py and string_multi_replace_node.py
patterns = []
for _, string_to_remove in removals:
    # Build pattern
    pattern = ...
    patterns.append(re.compile(pattern, flags=flags))

# Apply all patterns
for pattern in patterns:
    result = pattern.sub('', result)
```

**String Parsing (Multiline Input):**
Common pattern for parsing user input:
```python
strings_list = []
for line in strings_to_remove.splitlines():
    line = line.strip()
    if not line:
        continue
    strings_list.append(line)
```

**Case Sensitivity Handling:**
Consistent approach across nodes:
```python
flags = 0 if match_case else re.IGNORECASE
regex = re.compile(pattern, flags=flags)
```

---

*Convention analysis: 2026-03-03*
