## Journal content
Your journal entry should contain the following (you can use Obsedian if you like to set it up)

## <4/June>
#### Summary
This week, I developed a robust video text extraction method using OpenCV and Tesseract OCR. The primary goal was to identify text segments in videos and store the extracted text along with timestamps in a JSON file.
> What work did you do this week
The VideoTextExtractor code aims to extract text from videos and save the results as a JSON file, where each entry represents a text segment with timestamps and extracted text. 
- Overall logic flow:
    - Initialization: The code sets up the class with necessary parameters like video path, output JSON file path, and thresholds for frame difference and text similarity detection.
    - Frame Difference Analysis: The frame_difference function calculates the difference between consecutive video frames, returning a value indicating the visual change between frames.
    - Text Extraction from Frames: The extract_text function takes a single frame as input and uses Tesseract OCR to extract text from the frame.
    - Segment Identification: The find_segments function iterates through the video frames, calculating frame differences. When the difference exceeds a predefined threshold, it marks a potential segment boundary. It creates segment entries containing timestamps, frame numbers, and a flag indicating the presence of text.
    - Text Extraction from Segments: The extract_text_from_segments function iterates through the identified segments and extracts text from the starting frame of each segment using extract_text.
    - Segment Merging: The save_segments_to_json function combines segments that likely contain the same text by checking for text similarity using fuzzy matching. It updates the segment entries with the combined text and timestamps.
    - Saving Results: The final list of segments, with extracted text and timestamps, is saved to a JSON file using json.dump.
    - Process Video: The process_video function orchestrates the entire process by calling the functions mentioned above in order to complete the text extraction and saving.
Essentially, the code analyzes the video frames for visual changes to detect potential text segments. It then extracts text from these segments, merges overlapping segments based on text similarity, and saves the final results in a JSON format, allowing for easy access and analysis of the video text data.
> What work you are planning to do next week
- incorporate this into the app
- try improve accuracy of text detection and segment merging.
> Any blockers
- Currently, the script relies on a hardcoded path to the Tesseract executable. It would be more versatile to allow the user to specify the Tesseract path via a configuration file or command-line argument.

#### Issues and PRs
> Issue 1: Enhance video segment creation as right now the save_segments_to_json method within ocr_method.py correctly merges segments if text is present/similar to the next segments text. But we want it to also merge segments if there are consecutive segments without text (text_present = false).
> Issue 2: ocr_method has hardcoded tesseract path. Currently, this script uses a hardcoded path to point towards the tesseract executable, as of right now it needs to be removed.

#### Evidence
Mark all that applied this week
- [V] Attended class
- [V] Responded to PRs/Issues
- [V] Met with the team online. Forum Microsoft Teams
- [V] Commits to group repo

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?
- I implemented text similarity checking in save_segments_to_json to combine segments that likely contain the same text, improving the accuracy and usability of the extracted data.
> Did you discuss these ideas with the group? What was the outcome?
- I shared the code with the group and received feedback on the approach and implementation. We agreed that the fuzzy matching approach for segment merging was effective and helped to improve the overall accuracy.
> How did you validate your progress this week?
- I validated the code by testing it on a video file with different text content and complexities.
- I carefully examined the output JSON files to ensure that the identified segments and extracted text were somewhat accurate and properly formatted.


## <11/June>
#### Summary
This week, I focused on integrating JSON data containing OCR and LLM outputs with the video player application. The goal was to display the corresponding LLM output in the text panel whenever the video playback reaches the time range specified in the JSON file.
> What work did you do this week
- Modified VideoPlayer class to load the JSON file with the same name as the video file.
- Added logic to the update_timeline function to match the current video time with the time ranges in the JSON data.
- Implemented the ability to update the text panel with the corresponding LLM output.
> What work you are planning to do next week
- Implement the audio cues to indicate highlighted segments.
- Integrate other components (ocr_method, format_fidelity, code_identifier) as right now we are feeding a 'complete' json file but we want to incorporate the features of creating that json file.
> Any blockers
- Currently, the application assumes a JSON file exists with the same name as the video file. 

#### Issues and PRs
> N/A

#### Evidence
Mark all that applied this week
- [V] Attended class
- [V] Responded to PRs/Issues
- [V] Met with the team online. Forum Microsoft Teams
- [V] Commits to group repo

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?
- Initially, I considered displaying all JSON data in the text panel, but it quickly became apparent that it would be overwhelming for the user.
The current approach of dynamically updating the text panel based on the current video time provides a more user-friendly experience.
> Did you discuss these ideas with the group? What was the outcome?
- I discussed the design changes with the group and received positive feedback. We agreed that the dynamic text update approach is more intuitive. But we will incorporate a feature that does provide the whole code to the user which the user can access.
> How did you validate your progress this week?
- I validated my progress by testing the application with a video and JSON data. The application successfully displayed the correct LLM output for each time range.
- I also shared a preview with the group to gather feedback and ensure the changes were working as intended.