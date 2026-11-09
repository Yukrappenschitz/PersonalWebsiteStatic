
import unittest

from generate_page import(
    extract_title,

) 



class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_title(self):

        test_h1_header = "# Hello"

        self.assertEqual(
            extract_title(test_h1_header), 
            "Hello")




if __name__ == "__main__":
    unittest.main()