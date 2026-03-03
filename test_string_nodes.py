import unittest
from string_strip_node import StringStripNode
from string_multi_replace_node import StringMultiReplaceNode
from string_conditional_append_node import StringConditionalAppendNode
from string_contains_any_node import StringContainsAnyNode

class TestStringNodes(unittest.TestCase):
    def setUp(self):
        self.strip_node = StringStripNode()
        self.replace_node = StringMultiReplaceNode()
        self.append_node = StringConditionalAppendNode()
        self.contains_any_node = StringContainsAnyNode()

    def test_strip_basic_functionality(self):
        input_string = "This is a test string with test word"
        strings_to_remove = "test"
        result = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "This is a string with word")

    def test_strip_multiple_strings(self):
        input_string = "This is a test string with another test and More Text"
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
        self.assertEqual(result, "This is a string with another and")

    def test_strip_case_sensitivity(self):
        input_string = "Test TEST test"
        strings_to_remove = "test"

        # Case-insensitive
        result1 = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result1, "")

        # Case-sensitive
        result2 = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=True,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result2, "Test TEST")

    def test_strip_punctuation_preserved(self):
        # Test Issue #6 fix: punctuation should be preserved
        input_string = "Let's meet, Grandma!"
        strings_to_remove = "meet"
        result = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "Let's, Grandma!")

    def test_strip_punctuation_removed(self):
        # Test legacy behavior: punctuation removed
        input_string = "test, test: test. test; test"
        strings_to_remove = "test"
        result = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=False,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "")

    def test_replace_basic_functionality(self):
        input_string = "Hello world"
        replacement_pairs = "world::everyone"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "Hello everyone")

    def test_replace_multiple_pairs(self):
        input_string = "The quick brown fox jumps over the lazy dog"
        replacement_pairs = """quick::slow
        brown::black
        fox::cat"""
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "The slow black cat jumps over the lazy dog")

    def test_replace_case_sensitivity(self):
        input_string = "Hello HELLO hello"
        replacement_pairs = "hello::hi"

        # Case-insensitive
        result1 = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result1, "hi hi hi")

        # Case-sensitive
        result2 = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=True,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result2, "Hello HELLO hi")

    def test_replace_custom_delimiter(self):
        input_string = "Hello world"
        replacement_pairs = "world->everyone"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="->",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "Hello everyone")

    def test_replace_punctuation_preserved(self):
        # Test Issue #6 fix: punctuation preserved in replace
        input_string = "Let's meet, Grandma!"
        replacement_pairs = "meet::eat"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "Let's eat, Grandma!")

    def test_replace_prompt_syntax_preserved(self):
        # Test Issue #6: Prompt control syntax like [A1111:Forge:.5]
        input_string = "A prompt with [word1:word2:.5] syntax"
        replacement_pairs = "prompt::modified"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "A modified with [word1:word2:.5] syntax")

    def test_extra_spaces_handling(self):
        # Test for StringStripNode
        input_string = "This   is   a    test    string"
        strings_to_remove = "test"
        result1 = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result1, "This is a string")

        # Test for StringMultiReplaceNode
        replacement_pairs = "is::was"
        result2 = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result2, "This was a test string")

    # Tests for StringConditionalAppendNode (Issue #5)
    def test_append_string_not_found(self):
        # String not found, should append
        input_string = "Hello world"
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check="goodbye",
            position="end",
            match_case=False,
            separator=", "
        )
        self.assertEqual(result, "Hello world, goodbye")
        self.assertTrue(was_appended)

    def test_append_string_found(self):
        # String found, should not append
        input_string = "Hello world"
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check="world",
            position="end",
            match_case=False,
            separator=", "
        )
        self.assertEqual(result, "Hello world")
        self.assertFalse(was_appended)

    def test_append_beginning(self):
        # Append at beginning
        input_string = "world"
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check="Hello",
            position="beginning",
            match_case=False,
            separator=", "
        )
        self.assertEqual(result, "Hello, world")
        self.assertTrue(was_appended)

    def test_append_case_insensitive(self):
        # Case insensitive search
        input_string = "Hello WORLD"
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check="world",
            position="end",
            match_case=False,
            separator=", "
        )
        self.assertEqual(result, "Hello WORLD")
        self.assertFalse(was_appended)

    def test_append_case_sensitive(self):
        # Case sensitive search
        input_string = "Hello WORLD"
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check="world",
            position="end",
            match_case=True,
            separator=", "
        )
        self.assertEqual(result, "Hello WORLD, world")
        self.assertTrue(was_appended)

    def test_append_custom_separator(self):
        # Custom separator
        input_string = "Hello"
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check="world",
            position="end",
            match_case=False,
            separator=" | "
        )
        self.assertEqual(result, "Hello | world")
        self.assertTrue(was_appended)

    def test_append_no_separator(self):
        # No separator (empty string)
        input_string = "Hello"
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check="world",
            position="end",
            match_case=False,
            separator=""
        )
        self.assertEqual(result, "Helloworld")
        self.assertTrue(was_appended)

    def test_append_multiple_strings(self):
        # Multiple strings to check, some found, some not
        input_string = "Hello world"
        strings_to_check = """world
goodbye
thanks"""
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check=strings_to_check,
            position="end",
            match_case=False,
            separator=", "
        )
        # "world" is found, "goodbye" and "thanks" should be appended
        self.assertEqual(result, "Hello world, goodbye, thanks")
        self.assertTrue(was_appended)

    def test_append_multiple_all_found(self):
        # All strings found, nothing appended
        input_string = "Hello world goodbye"
        strings_to_check = """Hello
world
goodbye"""
        result, was_appended = self.append_node.conditional_append(
            input_string=input_string,
            strings_to_check=strings_to_check,
            position="end",
            match_case=False,
            separator=", "
        )
        self.assertEqual(result, "Hello world goodbye")
        self.assertFalse(was_appended)

    def test_replace_with_space(self):
        # Test Issue #8: Replace with space (trailing space should be preserved)
        input_string = "hello_world_test"
        replacement_pairs = "_:: "
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=False
        )[0]
        self.assertEqual(result, "hello world test")

    def test_replace_with_leading_space(self):
        # Test Issue #8: Replace with leading space
        input_string = "value1,value2,value3"
        replacement_pairs = ",::, "
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=False
        )[0]
        self.assertEqual(result, "value1, value2, value3")

    def test_replace_with_whitespace_only(self):
        # Test Issue #8: Replace with only whitespace
        input_string = "word1___word2"
        replacement_pairs = "___::   "
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=False
        )[0]
        self.assertEqual(result, "word1   word2")

    def test_replace_with_tab(self):
        # Test Issue #8: Replace with tab character
        input_string = "column1|column2|column3"
        replacement_pairs = "|::\t"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=False
        )[0]
        self.assertEqual(result, "column1\tcolumn2\tcolumn3")

    # Tests for StringContainsAnyNode (Issue #9)
    def test_contains_any_found(self):
        # Substring present, returns True
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful anime portrait",
            substrings="anime",
            match_case=False
        )
        self.assertTrue(result)
        self.assertEqual(matched, "anime")

    def test_contains_any_not_found(self):
        # No match, returns False
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful landscape",
            substrings="anime",
            match_case=False
        )
        self.assertFalse(result)
        self.assertEqual(matched, "")

    def test_contains_any_multiple_first_match(self):
        # Returns first matched substring
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful anime manga portrait",
            substrings="""cel-shaded
anime
manga""",
            match_case=False
        )
        self.assertTrue(result)
        self.assertEqual(matched, "anime")

    def test_contains_any_case_insensitive(self):
        # Default case-insensitive behavior
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful ANIME portrait",
            substrings="anime",
            match_case=False
        )
        self.assertTrue(result)
        self.assertEqual(matched, "anime")

    def test_contains_any_case_sensitive(self):
        # Case-sensitive matching
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful ANIME portrait",
            substrings="anime",
            match_case=True
        )
        self.assertFalse(result)
        self.assertEqual(matched, "")

    def test_contains_any_case_sensitive_found(self):
        # Case-sensitive matching with exact case
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful ANIME portrait",
            substrings="ANIME",
            match_case=True
        )
        self.assertTrue(result)
        self.assertEqual(matched, "ANIME")

    def test_contains_any_empty_input(self):
        # Empty input string
        result, matched = self.contains_any_node.contains_any(
            input_string="",
            substrings="anime",
            match_case=False
        )
        self.assertFalse(result)
        self.assertEqual(matched, "")

    def test_contains_any_empty_substrings(self):
        # Empty substrings
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful anime portrait",
            substrings="",
            match_case=False
        )
        self.assertFalse(result)
        self.assertEqual(matched, "")

    def test_contains_any_whitespace_substrings(self):
        # Substrings with only whitespace lines (should be ignored)
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful anime portrait",
            substrings="""
anime
   """,
            match_case=False
        )
        self.assertTrue(result)
        self.assertEqual(matched, "anime")

    def test_contains_any_partial_match(self):
        # Partial substring match (anime matches animation)
        result, matched = self.contains_any_node.contains_any(
            input_string="A beautiful animation",
            substrings="anim",
            match_case=False
        )
        self.assertTrue(result)
        self.assertEqual(matched, "anim")


    # Tests for sort_by_length parameter (Issue #11)
    def test_replace_sort_by_length_default(self):
        # Default behavior: longest match first prevents substring clobbering
        input_string = "this is a test"
        replacement_pairs = """is::WAS
this::THAT"""
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True,
            sort_by_length=True
        )[0]
        # "this" (4 chars) replaced before "is" (2 chars), so "this" is not mangled
        self.assertEqual(result, "THAT WAS a test")

    def test_replace_sort_by_length_disabled(self):
        # Input-order replacement: pairs processed in the order given
        input_string = "cat is here"
        replacement_pairs = """cat::dog
dog::fish"""
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True,
            sort_by_length=False
        )[0]
        # "cat" -> "dog" first, then "dog" -> "fish" (chained replacement)
        self.assertEqual(result, "fish is here")

    def test_replace_sort_by_length_enabled_no_chaining(self):
        # With sort enabled, equal-length pairs are sorted reverse-alphabetically,
        # so "dog::fish" runs before "cat::dog". Since "dog" isn't in the original
        # string, only "cat::dog" produces a match. No chaining occurs.
        input_string = "cat is here"
        replacement_pairs = """cat::dog
dog::fish"""
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            preserve_punctuation=True,
            remove_extra_spaces=True,
            sort_by_length=True
        )[0]
        self.assertEqual(result, "dog is here")

    # Tests for use_regex parameter (Issue #11)
    def test_replace_use_regex_basic(self):
        # Regex pattern matching
        input_string = "hello123world456"
        replacement_pairs = r"\d+:: "
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=False,
            use_regex=True
        )[0]
        self.assertEqual(result, "hello world ")

    def test_replace_use_regex_disabled(self):
        # Without regex, special chars are treated literally
        input_string = r"hello\d+world"
        replacement_pairs = r"\d+::REPLACED"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=True,
            use_regex=False
        )[0]
        self.assertEqual(result, "helloREPLACEDworld")

    def test_replace_use_regex_with_groups(self):
        # Regex with capture groups in replacement
        input_string = "2024-01-15"
        replacement_pairs = r"(\d{4})-(\d{2})-(\d{2})::\3/\2/\1"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=True,
            use_regex=True
        )[0]
        self.assertEqual(result, "15/01/2024")

    def test_replace_use_regex_character_class(self):
        # Regex with character class
        input_string = "Hello, World! How are you?"
        replacement_pairs = "[!?,]::;"
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=True,
            use_regex=True
        )[0]
        self.assertEqual(result, "Hello; World; How are you;")

    def test_replace_regex_with_input_order(self):
        # Combine regex + input-order for chained regex replacements
        input_string = "foo123bar456baz"
        replacement_pairs = r"""\d+::_
foo_bar::REPLACED"""
        result = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=False,
            preserve_punctuation=True,
            remove_extra_spaces=True,
            sort_by_length=False,
            use_regex=True
        )[0]
        # First: \d+ -> _ gives "foo_bar_baz"
        # Then: foo_bar -> REPLACED gives "REPLACED_baz"
        self.assertEqual(result, "REPLACED_baz")


if __name__ == '__main__':
    unittest.main()