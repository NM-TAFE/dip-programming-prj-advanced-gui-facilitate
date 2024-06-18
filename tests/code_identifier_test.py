import os
import unittest

from app.code_identifier import CodeIdentifier


class CodeIdentifierTestCase(unittest.TestCase):

    def setUp(self):
        self.code_identifier = CodeIdentifier("../app/code_identifier_dataset.csv")

    def test_text_oscar_wilde(self):
        text_the_picture_of_dorian_gray = ("The studio was filled with the rich odor of roses, and when the light "
                                           "summer wind stirred amidst the trees of the garden, there came through "
                                           "the open door the heavy scent of the lilac, or the more delicate perfume "
                                           "of the pink-flowering thorn.")
        detected = self.code_identifier.identify(text_the_picture_of_dorian_gray)

        self.assertEqual("Plain Text", detected)

    def test_python_class(self):
        text_python_class = "class CodeIdentifierTestCase(unittest.TestCase):"

        detected = self.code_identifier.identify(text_python_class)

        self.assertEqual("Python", detected)

    def test_empty_string(self):
        empty_string = ""
        detected = self.code_identifier.identify(empty_string)
        self.assertEqual("Plain Text", detected)

    def test_simple_function_definition(self):
        python_function = "def greet(name):\n    print(f'Hello, {name}!')"
        detected = self.code_identifier.identify(python_function)
        self.assertEqual("Python", detected)

    def test_loop_with_conditionals(self):
        python_code = ("for i in range(10):\n"
                       "    if i % 2 == 0:\n"
                       "        print(f'{i} is even')\n"
                       "    else:\n"
                       "        print(f'{i} is odd')")
        detected = self.code_identifier.identify(python_code)
        self.assertEqual("Python", detected)

    def test_class_with_methods(self):
        python_class = ("class Animal:\n"
                        "    def __init__(self, name):\n"
                        "        self.name = name\n"
                        "    def speak(self):\n"
                        "        pass\n"
                        "\n"
                        "class Dog(Animal):\n"
                        "    def speak(self):\n"
                        "        return 'Woof!'")
        detected = self.code_identifier.identify(python_class)
        self.assertEqual("Python", detected)

    def test_exception_handling(self):
        python_exception_handling = ("try:\n"
                                     "    1 / 0\n"
                                     "except ZeroDivisionError:\n"
                                     "    print('Cannot divide by zero!')\n"
                                     "except Exception as e:\n"
                                     "    print(f'An error occurred: {e}')")
        detected = self.code_identifier.identify(python_exception_handling)
        self.assertEqual("Python", detected)

    def test_famous_jokes(self):
        famous_joke = "Why don't eggs tell jokes? They'd crack each other up!"
        detected = self.code_identifier.identify(famous_joke)
        self.assertEqual("Plain Text", detected)

    def test_technical_documentation(self):
        technical_documentation = ("In this section, we discuss the architecture of the system. "
                                   "The system consists of three main components: the frontend, the backend, "
                                   "and the database.")
        detected = self.code_identifier.identify(technical_documentation)
        self.assertEqual("Plain Text", detected)

    def test_casual_conversation(self):
        casual_conversation = "Hey, how are you doing today? I'm planning to go to the park later."
        detected = self.code_identifier.identify(casual_conversation)
        self.assertEqual("Plain Text", detected)

    def test_special_characters_text(self):
        special_characters_text = "The quick brown fox jumps over the lazy dog! @#$%^&*()"
        detected = self.code_identifier.identify(special_characters_text)
        self.assertEqual("Plain Text", detected)

    def test_multiline_plain_text(self):
        multiline_plain_text = ("First line of text.\n"
                                "Second line of text.\n"
                                "Third line of text.")
        detected = self.code_identifier.identify(multiline_plain_text)
        self.assertEqual("Plain Text", detected)

    def test_multiline_python_code(self):
        multiline_python_code = ("def multiply(a, b):\n"
                                 "    result = a * b\n"
                                 "    return result\n"
                                 "\n"
                                 "print(multiply(2, 3))")
        detected = self.code_identifier.identify(multiline_python_code)
        self.assertEqual("Python", detected)


if __name__ == '__main__':
    unittest.main()
