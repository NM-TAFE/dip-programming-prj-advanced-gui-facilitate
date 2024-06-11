import openai
import cv2
import pytesseract
import logging
from typing import Union
import utils
from utils import config


class ExtractText:
    """
    A utility class for extracting and formatting code snippets from video frames using OCR and OpenAI.

    This class provides methods for extracting code from a video frame, formatting the code to match a
    specific programming language, and utilizing the OpenAI language model for code correction.

    Note:
    This class assumes the availability of the OpenAI GPT-3.5 Turbo model and PyTesseract for OCR.
    """

    @staticmethod
    def extract_code_at_timestamp(filename: str, timestamp: float) -> str:
        """
        Extract formatted code from a video file at a given frame.
        :param filename: File path of the video to extract the frame from
        :param timestamp: Time stamp of the frame to extract
        :return: Formatted code as a string
        """
        frame = ExtractText.extract_frame_at_timestamp(filename, timestamp)
        if frame is not None:
            extracted_text = pytesseract.image_to_string(frame)
            logging.info(f"Successfully extracted code from frame @ {timestamp}s in file {filename}")
            return ExtractText.format_raw_ocr_string(extracted_text)
        else:
            logging.error(f"Unable to extract code from frame @ {timestamp}s in file {filename}")
            return "ERROR"

    @staticmethod
    def format_raw_ocr_string(extracted_text: str) -> str:
        """
        Attempts to format a given string to match given programming language
        :param extracted_text: Raw OCR text to format
        :return: Formatted text as string
        """
        language = config("UserSettings", "programming_language")
        formatted_text = extracted_text
        if config("Formatting", "openai_analysis"):
            formatted_text = ExtractText.openai_format_raw_ocr(formatted_text, language)
        if config("Formatting", "remove_backticks"):
            formatted_text = formatted_text.replace("```", "")
        if config("Formatting", "remove_language_name"):
            formatted_text = formatted_text.replace(language, "", 1)
        return formatted_text

    @staticmethod
    def extract_frame_at_timestamp(filename: str, timestamp: float) -> Union[cv2.VideoCapture, None]:
        """
        Extract a frame from a video at a given timestamp
        :param filename: File path to extract frame from
        :param timestamp: Timestamp to extract the frame from
        :return: Returns capture frame or None
        """
        cap = cv2.VideoCapture(f"{utils.get_vid_save_path()}{filename}")
        if not cap.isOpened():
            logging.error(f"Failed to open {filename} stream")
            return None
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        ret, frame = cap.read()
        if ret:
            cap.release()
            logging.info(f"Successfully captured frame @ {timestamp}s in file {filename}")
            return frame
        else:
            logging.error(f"Failed to capture frame @ {timestamp}s in file {filename}")
            return None

    @staticmethod
    def openai_format_raw_ocr(extracted_text: str, language: str) -> str:
        """
        "Given an input of potentially raw OCR capture from a video containing Python code, your task is to correct
        and format the code. Ensure the code's indentation and syntax are accurate. Exclude any content that isn't
        valid Python code. If no recognizable Python content is detected, return 'ERROR'. Do not provide
        explanations, leading or trailing backticks, or specify the language in your response. Simply return the
        corrected code. Avoid making extensive alterations; the goal is to retain the original intent of the capture
        as closely as possible."

        prompt = f"Fix up the following {language} code snippet: '{extracted_text}'" response =
        openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[ {"role": "system", "content": "Given an input
        of potentially raw OCR capture from a video containing code, your task is to correct and format the code.
        Ensure the code's indentation and syntax are accurate. Exclude any content that isn't valid for the specified
        language. If no recognizable content is detected, return 'ERROR'. Do not provide explanations, leading or
        trailing backticks, or specify the language in your response. Simply return the corrected code. Avoid making
        extensive alterations; the goal is to retain the original intent of the capture as closely as possible."},
        {"role": "user", "content": prompt} ] ) return response.choices[0].message['content']

        Format given text using OpenAI language model API
        :param extracted_text: Raw extracted text to format
        :param language: Programming language to format the raw text as
        :return: Formatted code as string
        """
        try:
            prompt = f"Fix up the following {language} code snippet, fix up any indentation errors, syntax errors, " \
                     f"and anything else that is incorrect: '{extracted_text}'"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"You are a coding assistant. You reply only in {language} code "
                                "that is correct and formatted. Do NOT reply with any explanation, "
                                f"only code. If you are given something that is not {language} code, "
                                "you must NOT include it in your response. If nothing is present, "
                                "simply return 'ERROR' and nothing else. Do NOT return leading or "
                                "trailing"
                                "backticks and do NOT return the language before the code snippet."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content']
        except openai.OpenAIError as error:
            logging.exception(error)
            return extracted_text
