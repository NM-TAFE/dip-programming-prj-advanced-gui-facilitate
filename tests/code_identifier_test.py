import os
import unittest

from app.code_identifier import CodeIdentifier


class CodeIdentifierTestCase(unittest.TestCase):
    """
    Unit tests for the CodeIdentifier class.
    """
    def test_text_oscar_wilde(self):
        """
        Test identifying plain text from a literary passage.
        """
        text_the_picture_of_dorian_gray = ("The studio was filled with the rich odor of roses, and when the light "
                                           "summer wind stirred amidst the trees of the garden, there came through "
                                           "the open door the heavy scent of the lilac, or the more delicate perfume "
                                           "of the pink-flowering thorn.")
        code_identifier = CodeIdentifier("../app/code_identifier_dataset.csv")
        detected = code_identifier.identify(text_the_picture_of_dorian_gray)

        self.assertEqual("Plain Text", detected)

    def test_python_class(self):
        """
        Test identifying Python code.
        """
        text_python_class = "class CodeIdentifierTestCase(unittest.TestCase):"
        code_identifier = CodeIdentifier("../app/code_identifier_dataset.csv")
        detected = code_identifier.identify(text_python_class)

        self.assertEqual("Python", detected)


if __name__ == '__main__':
    unittest.main()
