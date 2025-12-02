import unittest
from string_strip_node import StringStripNode
from string_multi_replace_node import StringMultiReplaceNode
from string_conditional_append_node import StringConditionalAppendNode

class TestStringNodes(unittest.TestCase):
    def setUp(self):
        self.strip_node = StringStripNode()
        self.replace_node = StringMultiReplaceNode()
        self.append_node = StringConditionalAppendNode()

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

if __name__ == '__main__':
    unittest.main()