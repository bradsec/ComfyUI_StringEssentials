import unittest
from string_strip_node import StringStripNode
from string_replace_node import StringReplaceNode

class TestStringNodes(unittest.TestCase):
    def setUp(self):
        self.strip_node = StringStripNode()
        self.replace_node = StringReplaceNode()

    def test_strip_basic_functionality(self):
        input_string = "This is a test string with test word"
        strings_to_remove = "test"
        result = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
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
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result1, "")
        
        # Case-sensitive
        result2 = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=True,
            match_whole_string=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result2, "Test TEST")

    def test_strip_punctuation_handling(self):
        input_string = "test, test: test. test; test"
        strings_to_remove = "test"
        result = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
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
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result, "Hello everyone")

    def test_extra_spaces_handling(self):
        # Test for StringStripNode
        input_string = "This   is   a    test    string"
        strings_to_remove = "test"
        result1 = self.strip_node.string_strip(
            input_string=input_string,
            strings_to_remove=strings_to_remove,
            match_case=False,
            match_whole_string=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result1, "This is a string")
        
        # Test for StringReplaceNode
        replacement_pairs = "is::was"
        result2 = self.replace_node.string_replace(
            input_string=input_string,
            replacement_pairs=replacement_pairs,
            replacement_delimiter="::",
            match_case=False,
            match_whole_string=True,
            remove_extra_spaces=True
        )[0]
        self.assertEqual(result2, "This was a test string")

if __name__ == '__main__':
    unittest.main()