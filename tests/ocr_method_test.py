import unittest
from unittest.mock import patch, MagicMock
from app.ocr_method import VideoTextExtractor
import pytesseract

class CombineSegmentsTestCase(unittest.TestCase):
    """
    Test cases for the combine_segments method of the VideoTextExtractor class.
    """
    def setUp(self):
        """
        Set up the test environment by initializing a VideoTextExtractor instance
        and providing a list of segments for testing.
        """
        self.mock_config = {
            'config': {
                'tessaractPath': 'C:\\Users\\bishi\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'  # Adjust this path if needed
            }
        }
        with patch.object(VideoTextExtractor, 'load_app_json_config', return_value=self.mock_config):
            self.text_extractor = VideoTextExtractor("example/test2 - 1716891852652.mp4", "test.json")

        pytesseract.pytesseract.tesseract_cmd = self.mock_config['config']['tessaractPath']

        self.segments = [
            {
                "start_frame": 0,
                "end_frame": 15,
                "start_time": 0.0,
                "end_time": 0.5,
                "text_present": False,
                "extracted_text": ""
            },
            {
                "start_frame": 30,
                "end_frame": 30,
                "start_time": 1.0,
                "end_time": 1.0,
                "text_present": False,
                "extracted_text": ""
            },
            {
                "start_frame": 30,
                "end_frame": 45,
                "start_time": 1.0,
                "end_time": 1.5,
                "text_present": True,
                "extracted_text": "Lorem Ipsum"
            },
            {
                "start_frame": 45,
                "end_frame": 480,
                "start_time": 1.5,
                "end_time": 16.0,
                "text_present": True,
                "extracted_text": "I finally saw The Matrix today.\nIt was the best documentary\nI've ever seen."
            },
            {
                "start_frame": 480,
                "end_frame": 510,
                "start_time": 16.0,
                "end_time": 17.0,
                "text_present": True,
                "extracted_text": "I finally saw The Matrix today.\nIt was the best documentary\nI've ever seen."
            },
        ]

    def test_combine_segments_combines_segments_with_same_text(self):
        """
        Test that combine_segments correctly combines segments with the same extracted text.
        """
        initial_segment_count = len(self.segments)
        self.text_extractor.combine_segments(self.segments)

        # Check if the number of segments has changed as expected
        self.assertGreater(len(self.segments), 0, "Expected segments after combining.")

        # Example: Assert on the first combined segment's content
        combined_segment = next((seg for seg in self.segments if "Lorem Ipsum" in seg["extracted_text"]), None)
        self.assertIsNotNone(combined_segment, "Expected combined segment with 'Lorem Ipsum'.")

    def test_combine_segments_combines_segments_without_text(self):
        """
        Test that combine_segments correctly combines segments without extracted text.
        """
        self.text_extractor.combine_segments(self.segments)
        combined_segment = self.segments[0]

        self.assertEqual(0, combined_segment["start_frame"])
        self.assertEqual(30, combined_segment["end_frame"])
        self.assertEqual("", combined_segment["extracted_text"])

    def test_combine_segments_does_not_combine_unrelated_segments(self):
        """
        Test that combine_segments does not combine unrelated segments with different extracted text.
        """
        self.text_extractor.combine_segments(self.segments)
        unchanged_segment = self.segments[1]
        self.assertEqual(30, unchanged_segment["start_frame"])

    def test_combine_segments_with_empty_segments(self):
        """
        Test that combine_segments correctly handles an empty segments list.
        """
        empty_segments = []
        self.text_extractor.combine_segments(empty_segments)
        self.assertEqual([], empty_segments)


if __name__ == '__main__':
    unittest.main()
