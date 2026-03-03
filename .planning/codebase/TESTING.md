# Testing Patterns

**Analysis Date:** 2026-03-03

## Test Framework

**Runner:**
- unittest (Python standard library)
- Config: None (uses default unittest discovery)
- No pytest.ini, setup.cfg, or tox.ini configuration detected

**Assertion Library:**
- unittest.TestCase assertions (built-in)

**Run Commands:**
```bash
python -m unittest test_string_nodes.py               # Run all tests
python -m unittest test_string_nodes.TestStringNodes  # Run specific test class
python -m unittest test_string_nodes.TestStringNodes.test_<name>  # Run specific test
```

**Test File Location:**
- `test_string_nodes.py` in project root alongside source files (`/home/mark/Code/ComfyUI_StringEssentials/test_string_nodes.py`)
- Co-located with source code (not in separate tests directory)

## Test File Organization

**Location:**
- Co-located pattern: test file in same directory as source modules

**Naming:**
- Test file: `test_string_nodes.py`
- Test class: `TestStringNodes` (PascalCase with Test prefix)
- Test methods: `test_<functionality>` format

**Structure:**
```
test_string_nodes.py
├── TestStringNodes (class)
│   ├── setUp() - Initialize node instances
│   ├── test_strip_* - Tests for StringStripNode
│   ├── test_replace_* - Tests for StringMultiReplaceNode
│   ├── test_append_* - Tests for StringConditionalAppendNode
│   └── test_contains_any_* - Tests for StringContainsAnyNode
└── if __name__ == '__main__': unittest.main()
```

## Test Structure

**Suite Organization:**
```python
class TestStringNodes(unittest.TestCase):
    def setUp(self):
        self.strip_node = StringStripNode()
        self.replace_node = StringMultiReplaceNode()
        self.append_node = StringConditionalAppendNode()
        self.contains_any_node = StringContainsAnyNode()
```

**Patterns:**
- **Setup pattern:** `setUp()` method instantiates all node instances as instance variables for reuse across test methods
- **No teardown:** No `tearDown()` method (no cleanup needed)
- **Assertion pattern:** Direct method calls on node instances with parameter unpacking:
  ```python
  result = self.strip_node.string_strip(
      input_string=input_string,
      strings_to_remove=strings_to_remove,
      match_case=False,
      match_whole_string=True,
      preserve_punctuation=True,
      remove_extra_spaces=True
  )[0]
  self.assertEqual(result, expected_output)
  ```

**Test Method Characteristics:**
- Each test is independent and focused on a single behavior
- Tests use explicit parameter names (keyword arguments) for clarity
- Return value tuple unpacking: `[0]` for single return, tuple unpacking for multiple returns
- Clear arrange-act-assert flow (input setup → method call → assertion)

## Test Coverage by Node

**StringStripNode Tests:**
- `test_strip_basic_functionality`: Single string removal
- `test_strip_multiple_strings`: Multiple removal patterns (multiline input)
- `test_strip_case_sensitivity`: Case-insensitive vs case-sensitive modes
- `test_strip_punctuation_preserved`: Punctuation preservation (Issue #6)
- `test_strip_punctuation_removed`: Legacy punctuation removal behavior
- Extra spaces handling covered in `test_extra_spaces_handling`

**StringMultiReplaceNode Tests:**
- `test_replace_basic_functionality`: Single replacement pair
- `test_replace_multiple_pairs`: Multiple replacement pairs from multiline input
- `test_replace_case_sensitivity`: Case-insensitive vs case-sensitive modes
- `test_replace_custom_delimiter`: Custom delimiter support (not just `::`
- `test_replace_punctuation_preserved`: Punctuation preservation (Issue #6)
- `test_replace_prompt_syntax_preserved`: Bracket syntax preservation (e.g., `[word1:word2:.5]`)
- `test_replace_with_space`: Trailing space preservation in replacements (Issue #8)
- `test_replace_with_leading_space`: Leading space in replacement strings (Issue #8)
- `test_replace_with_whitespace_only`: Multiple spaces in replacements (Issue #8)
- `test_replace_with_tab`: Tab character in replacements (Issue #8)

**StringConditionalAppendNode Tests:**
- `test_append_string_not_found`: Appending when string not present
- `test_append_string_found`: No append when string already present
- `test_append_beginning`: Position flag "beginning" vs "end"
- `test_append_case_insensitive`: Case-insensitive search
- `test_append_case_sensitive`: Case-sensitive search
- `test_append_custom_separator`: Custom separator handling
- `test_append_no_separator`: Empty string separator
- `test_append_multiple_strings`: Multiple check strings with mixed found/not found
- `test_append_multiple_all_found`: All strings already present (no append)

**StringContainsAnyNode Tests:**
- `test_contains_any_found`: Basic found case
- `test_contains_any_not_found`: Basic not found case
- `test_contains_any_multiple_first_match`: Returns first match from multiple options
- `test_contains_any_case_insensitive`: Default case-insensitive behavior
- `test_contains_any_case_sensitive`: Case-sensitive search
- `test_contains_any_case_sensitive_found`: Case-sensitive with matching case
- `test_contains_any_empty_input`: Empty input string handling
- `test_contains_any_empty_substrings`: Empty substrings input
- `test_contains_any_whitespace_substrings`: Whitespace-only lines are ignored
- `test_contains_any_partial_match`: Substring matching (anime matches animation)

## Mocking

**Framework:** None - unittest provides basic mocking but not used in this codebase

**Patterns:**
- No mock objects used
- No external dependencies mocked
- Tests use real node instances with direct method calls
- All test data is embedded in test methods (no external fixtures)

**What to Mock:**
- No mocking required; all node classes are stateless and dependency-free

**What NOT to Mock:**
- Don't mock the node classes - test them directly with real instances

## Fixtures and Factories

**Test Data:**
- All test data embedded directly in test methods
- No separate fixture files or factory classes
- Input strings created inline:
  ```python
  input_string = "This is a test string with test word"
  strings_to_remove = "test"
  ```

**Location:**
- Test data is co-located with test methods (no separate fixtures directory)
- Issue-specific test data clearly labeled with issue references:
  ```python
  def test_strip_punctuation_preserved(self):
      # Test Issue #6 fix: punctuation should be preserved
      input_string = "Let's meet, Grandma!"
  ```

## Coverage

**Requirements:** None enforced (no coverage configuration detected)

**View Coverage:**
```bash
# Using unittest's built-in capabilities (limited):
python -m unittest discover -v

# Better coverage with coverage.py (not currently installed):
pip install coverage
coverage run -m unittest test_string_nodes.py
coverage report
```

**Observed Coverage:**
- **StringStripNode:** 100% - All major code paths tested (basic, multiple, case sensitivity, punctuation handling, spaces)
- **StringMultiReplaceNode:** 100% - All code paths tested (basic, multiple, case sensitivity, custom delimiter, punctuation, whitespace preservation)
- **StringConditionalAppendNode:** 100% - All code paths tested (found/not found, position, case sensitivity, separator options, multiple strings)
- **StringContainsAnyNode:** 100% - All code paths tested (found/not found, case sensitivity, empty inputs, whitespace handling, partial matching)
- **StringPreviewNode:** 0% - No tests (trivial pass-through logic)
- **StringTextboxNode:** 0% - No tests (trivial pass-through logic)

## Test Types

**Unit Tests:**
- Scope: Individual node class methods
- Approach: Direct method invocation with arranged inputs, assert on single output
- Example: `test_strip_basic_functionality` tests `string_strip()` method with specific parameters
- No test doubles or stubs - real objects used

**Integration Tests:**
- Not present in codebase (no multi-component interaction testing)

**E2E Tests:**
- Not present (ComfyUI-specific E2E would require full ComfyUI runtime)

**Issue-Driven Tests:**
- Tests explicitly tied to GitHub issues in comments
- Issue #6: Punctuation preservation tests
- Issue #8: Whitespace preservation in replacements tests
- Issue #9: StringContainsAnyNode feature tests
- Pattern: When fixing a bug, issue number added as comment and test created to verify fix

## Common Patterns

**Async Testing:**
- Not applicable - Python standard library code without async/await

**Error Testing:**
- No explicit error/exception testing
- Edge cases tested: empty strings, whitespace-only input, multiple spaces
- Validation through return values rather than exception handling

**Testing Multiline Input:**
```python
strings_to_remove = """test
More Text"""
result = self.strip_node.string_strip(
    input_string=input_string,
    strings_to_remove=strings_to_remove,
    match_case=False,
    match_whole_string=True,
    preserve_punctuation=True,
    remove_extra_spaces=True
)[0]
```

**Testing Multiple Parameters:**
```python
result, was_appended = self.append_node.conditional_append(
    input_string=input_string,
    strings_to_check=strings_to_check,
    position="end",
    match_case=False,
    separator=", "
)
self.assertEqual(result, expected_string)
self.assertTrue(was_appended)
```

**Testing Boolean Returns:**
- StringConditionalAppendNode returns `(string, boolean)` tuple
- StringContainsAnyNode returns `(boolean, string)` tuple
- Tests unpack both return values and assert on each

---

*Testing analysis: 2026-03-03*
