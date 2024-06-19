import unittest
from app import TextPanel 

class TestTextPanel(unittest.TestCase):

    def set_up(self):
        self.text_panel = TextPanel(None) 

    def test_initial_chat_history(self):
        self.assertTrue(self.text_panel.is_chat_history_empty())
        self.assertEqual(self.text_panel.retrieve_last_chat_history(), '')

    def test_add_and_retrieve_history(self):
        self.text_panel.add_to_chat_history("Message 1")
        self.text_panel.add_to_chat_history("Message 2")
        self.assertEqual(self.text_panel.retrieve_last_chat_history(), "Message 2")

    def test_empty_history(self):
        self.assertEqual(self.text_panel.retrieve_last_chat_history(), '')


if __name__ == '__main__':
    unittest.main()

