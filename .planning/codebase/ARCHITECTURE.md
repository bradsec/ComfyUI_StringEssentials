# Architecture

**Analysis Date:** 2026-03-03

## Pattern Overview

**Overall:** Node-based plugin architecture for ComfyUI

**Key Characteristics:**
- Modular node design where each node implements ComfyUI's node interface
- Each node is a standalone class with INPUT_TYPES, RETURN_TYPES, and execution methods
- Nodes are registered in a central registry for ComfyUI framework discovery
- String processing operations implemented using Python's `re` module for regex patterns
- No external dependencies beyond Python standard library
- Plugin loaded via `__init__.py` which exports node mappings

## Layers

**Node Layer:**
- Purpose: Implements individual string manipulation operations
- Location: Root directory - `string_textbox_node.py`, `string_strip_node.py`, `string_multi_replace_node.py`, `string_preview_node.py`, `string_conditional_append_node.py`, `string_contains_any_node.py`
- Contains: Node classes inheriting ComfyUI's node interface
- Depends on: Python `re` module for regex operations
- Used by: ComfyUI framework (loads via NODE_CLASS_MAPPINGS)

**Plugin Registry Layer:**
- Purpose: Provides node discovery and registration for ComfyUI
- Location: `__init__.py`
- Contains: NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS, WEB_DIRECTORY exports
- Depends on: All node modules
- Used by: ComfyUI framework at startup

**Testing Layer:**
- Purpose: Unit tests for all node functionalities
- Location: `test_string_nodes.py`
- Contains: unittest.TestCase subclass with comprehensive test suites
- Depends on: All node classes
- Used by: Developers running tests locally

## Data Flow

**String Processing Pipeline:**

1. Input received via `INPUT_TYPES` - user specifies string and processing parameters
2. ComfyUI calls node's FUNCTION method (e.g., `string_strip`, `string_replace`)
3. Processing method performs regex-based transformations
4. Optional cleanup via `cleanup_text()` if `remove_extra_spaces` is True
5. Return processed string(s) via RETURN_TYPES tuple

**Example - StringStripNode flow:**
1. User provides `input_string` and `strings_to_remove` (multiline)
2. `string_strip()` method parses removal list, sorted by length (longest first)
3. Regex patterns compiled with case sensitivity flags
4. Patterns applied sequentially to input string
5. Cleanup normalizes whitespace if enabled
6. Result returned as single-element tuple

**Example - StringConditionalAppendNode flow:**
1. User provides `input_string` and `strings_to_check` (multiline)
2. `conditional_append()` parses check list
3. Each string checked for presence in result (with case sensitivity option)
4. Missing strings appended at specified position (beginning/end)
5. Returns tuple of (modified_string, was_appended boolean)

**State Management:**
- Stateless nodes - each execution independent
- No shared state between invocations
- Only state change: modifying the input string passed through

## Key Abstractions

**Node Interface Pattern:**
- Purpose: Standardizes how nodes interact with ComfyUI framework
- Examples: `StringTextboxNode` (`string_textbox_node.py`), `StringStripNode` (`string_strip_node.py`)
- Pattern: Each node class implements three key class attributes:
  - `INPUT_TYPES()` classmethod - declares input parameters and their types
  - `RETURN_TYPES` tuple - declares output types
  - `FUNCTION` string - method name to call for execution
  - Execution method - performs actual processing and returns tuple

**Text Processing Pattern:**
- Purpose: Shared approach for string matching and replacement across nodes
- Examples: `string_strip_node.py`, `string_multi_replace_node.py`
- Pattern: Uses `re.compile()` with configurable flags (IGNORECASE), patterns include:
  - Word boundary matching: `\b` for whole word matching
  - Punctuation handling: conditional patterns with `(?:[,;:.])` for preservation/removal
  - Regex escaping: `re.escape()` to treat user input as literals

**Text Cleanup Pattern:**
- Purpose: Normalize whitespace after text modifications
- Examples: `cleanup_text()` method in `string_strip_node.py`, `string_multi_replace_node.py`
- Pattern: Two-step regex approach:
  1. Remove spaces before punctuation: `r'\s+([,;:.])'` → `r'\1'`
  2. Normalize multiple spaces: `r'\s{2,}'` → `' '`
  3. Strip leading/trailing whitespace

**Multi-value Processing Pattern:**
- Purpose: Handle comma-separated or line-separated lists of values
- Examples: All nodes with multiline string inputs
- Pattern: `.splitlines()` to split input, `.strip()` to clean each line, filter empty strings

## Entry Points

**ComfyUI Framework Loading:**
- Location: `__init__.py`
- Triggers: ComfyUI startup/refresh
- Responsibilities:
  - Imports all node classes
  - Exports NODE_CLASS_MAPPINGS for framework discovery
  - Exports NODE_DISPLAY_NAME_MAPPINGS for UI display names
  - Exports WEB_DIRECTORY for any client-side assets

**Individual Node Execution:**
- Location: Each node's FUNCTION method (e.g., `string_strip()` in `string_strip_node.py`)
- Triggers: ComfyUI workflow execution when node is evaluated
- Responsibilities:
  - Accept parameters from INPUT_TYPES
  - Perform string processing
  - Return results as tuple matching RETURN_TYPES

**Output Display:**
- Location: `string_preview_node.py` - StringPreviewNode
- Triggers: Workflow execution
- Responsibilities:
  - Display string output in UI via `preview_string()` method
  - Force re-evaluation on every execution via `IS_CHANGED()` returning NaN
  - Return both UI display data and result tuple

## Error Handling

**Strategy:** Defensive programming - validate and handle edge cases gracefully

**Patterns:**
- Empty input handling: All nodes check for empty strings and return sensible defaults
  - Example: `string_contains_any_node.py` line 40-41 returns `(False, "")` for empty substrings
  - Example: `string_conditional_append_node.py` line 44-45 returns unchanged input if no strings to check
- Line parsing robustness: `.strip()` applied to each line, whitespace-only lines filtered
  - Example: `string_strip_node.py` line 36-38 skips empty/whitespace lines in removal list
- Regex compilation safety: `re.escape()` used to prevent regex injection from user input
  - Example: `string_strip_node.py` line 55, 62 escape user strings before pattern compilation
- Delimiter handling: Split with `maxsplit=1` to allow delimiter characters in replacement text
  - Example: `string_multi_replace_node.py` line 42 uses `split(delimiter, 1)` to preserve right side

## Cross-Cutting Concerns

**Logging:** Not implemented - ComfyUI framework handles logging

**Validation:**
- User input validation occurs at parsing stage (splitlines, strip, filter empty)
- Type validation handled by ComfyUI framework via INPUT_TYPES/RETURN_TYPES declarations
- No explicit validation errors thrown; nodes handle edge cases gracefully

**Authentication:** Not applicable - nodes are part of ComfyUI plugin

**Case Sensitivity:**
- All text nodes support configurable case-sensitive matching via `match_case` boolean parameter
- Implemented via `re.IGNORECASE` flag when `match_case=False`
- Example: `string_strip_node.py` line 47 sets `flags = 0 if match_case else re.IGNORECASE`

**Punctuation Handling:**
- Special feature introduced to preserve punctuation adjacent to matched text
- Controlled by `preserve_punctuation` boolean parameter
- Enabled by default in most nodes for safe prompt/syntax handling
- Example: `string_strip_node.py` lines 53-65 show pattern variants for punctuation preservation

---

*Architecture analysis: 2026-03-03*
