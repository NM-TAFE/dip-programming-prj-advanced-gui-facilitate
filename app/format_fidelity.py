import openai
import logging

# api_key = 'sk-proj-su2RLa8r7VWi1CBSlyQ9T3BlbkFJCmRhVkjPSSyv37sjr8xY'


class CodeFormatter:
    def __init__(self, api_key: str):
        """
        Initialize the CodeFormatter with the provided OpenAI API key.

        :param api_key: OpenAI API key for authenticating requests.
        """
        openai.api_key = api_key

    def format_code(self, extracted_text: str, language: str) -> str:
        """
        Given an input of potentially raw OCR capture from a video containing Python code,
        correct and format the code. Ensure the code's indentation and syntax are accurate.

        :param extracted_text: Raw extracted text to format.
        :param language: Programming language to format the raw text as.
        :return: Formatted code as a string.
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
                                "trailing backticks and do NOT return the language before the code snippet."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content']
        except openai.OpenAIError as error:
            logging.exception(error)
            return extracted_text


# Example usage:
# formatter = CodeFormatter(api_key)
# formatted_code = formatter.format_code(extracted_text='some raw OCR text', language='Python')
# print(formatted_code)
