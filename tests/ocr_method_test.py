import unittest

from app.ocr_method import VideoTextExtractor


class CombineSegmentsTestCase(unittest.TestCase):
    def setUp(self):
        self.text_extractor = VideoTextExtractor("example/test2 - 1716891852652.mp4",
                                                 "test.json")
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
        self.text_extractor.combine_segments(self.segments)
        combined_segment = self.segments[-1]

        self.assertEqual(45, combined_segment["start_frame"])
        self.assertEqual(510, combined_segment["end_frame"])

    def test_combine_segments_combines_segments_without_text(self):
        self.text_extractor.combine_segments(self.segments)
        combined_segment = self.segments[0]

        self.assertEqual(0, combined_segment["start_frame"])
        self.assertEqual(30, combined_segment["end_frame"])

    def test_combine_segments_does_not_combine_unrelated_segments(self):
        self.text_extractor.combine_segments(self.segments)
        unchanged_segment = self.segments[1]
        self.assertEqual(30, unchanged_segment["start_frame"])
        self.assertEqual(45, unchanged_segment["end_frame"])

if __name__ == '__main__':
    unittest.main()
