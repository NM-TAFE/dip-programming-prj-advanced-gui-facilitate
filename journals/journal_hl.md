## Journal content
Your journal entry should contain the following (you can use Obsedian if you like to set it up)

## <7/May>
#### Summary
> What work did you do this week
- During the class, our team(Team facilitate) has had a chat for how to improve ocr visually and functionally for visual impairment people who need a code script from video. 
- Looked into Tesseract OCR to see how it works and how convenient to control the Tesseract for visual impairment people.
- Considered which way of improvements are more helpful for visual impairment people in either faster processing in scanning, scripting, and formatting code snippet or better accessibility in UI/UX.
- Looked into a research document focused on the performance of OCR depending on varying video quality and large language models.
>What work you are planning to do next week
- Still need to find out more discomfort of visual impairment people (I don't think we are fully understanding how difficult those people would be handling the Tesseract OCR)

> Any blockers
- Getting OpenAI API


#### Issues and PRs
> N/A

#### Evidence
Mark all that applied this week
- [V] Attended class
- [] Responded to PRs/Issues
- [V] Met with the team online. Forum Microsoft Teams
- [] Commits to group repo

> warning: If you were not able to mark any of these on a particular week, please email your lecturer with the reason.

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?
- I didn't have a firm idea yet.
> Did you discuss these ideas with the group? What was the outcome?
- I didn't discuss anything.
> How did you validate your progress this week?
- I didn't





## <14/May>
#### Summary
> What work did you do this week
- Participated in Key User Stories, acting and thinking as a visually impaired person, 'What I would like to do with Tesseract OCR', 'what could be better in utilising Tesseract OCR and screen reader.'
- 
>What work you are planning to do next week
- Feasibility check for pre-processing downloaded video to generate a code snippet and to add timestamps when a code block begins and ends.
- Making viable solution that doesn't require OpenAI(Chatgpt)
- Considering performance impact for realtime OCR

> Any blockers
- Getting OpenAI API(pricing)
- UI not navigable
- Hotkey issues
- Downloading video required
- Too much configuration to work
- Poor directory structure in code base



#### Issues and PRs
> N/A

#### Evidence
Mark all that applied this week
- [V] Attended class
- [] Responded to PRs/Issues
- [V] Met with the team online. Forum Microsoft Teams
- [] Commits to group repo

> warning: If you were not able to mark any of these on a particular week, please email your lecturer with the reason.

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?
- In case of bad internet connection, for the realtime code scan-script-generate process slow internet speed could change youtube video quality and could lead to lower accuracy of transcript as OCR has limited ability of scanning from low quality screen or video.  
> Did you discuss these ideas with the group? What was the outcome?
- At the moment, we are dealing with only downloaded video, we still can choose video quality to download    
> How did you validate your progress this week?
- I have been searching for viable solution without using openAI and Tesseract as our group is aiming to make it, finding out other LLM or seeing if we can make our own.




## <21/May>
#### Summary
> What work did you do this week
- Considered converting the Flask app to a desktop app instead.
- Searching and testing new LLM (Ollama, Llama 3, 4.7Gb model) to try to replace existing openAI then checking CPU usage and its response speed.
- Considered what issues I can indentify for CertIV students to contribute. 
>What work you are planning to do next week
- Finding out any ways to improve performance in CPU usage and response time.
- Searching for how to apply multiple OCRs to identify code frame and add timestamps, and with other OCR to extract and convert text to code.

> Any blockers
- Unexpected slow response speed of Llama 3 model and fairly high CPU usage
- Recognition accuracy of detecting differences in code 




#### Issues and PRs
> N/A

#### Evidence
Mark all that applied this week
- [V] Attended class
- [] Responded to PRs/Issues
- [V] Met with the team online. Forum Microsoft Teams
- [] Commits to group repo

> warning: If you were not able to mark any of these on a particular week, please email your lecturer with the reason.

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?
- Personally think that using various of Ollama models could be more beneficial in pricing and performance rather than training our own LLM or relying on GPT 3.5.   
> Did you discuss these ideas with the group? What was the outcome?
- I need more time to test more models and to see if it can be more useful and replaceable in actual use.     
> How did you validate your progress this week?
- I've downloaded some models of Ollama and tested them on my PC.




## <28/May>
#### Summary
> What work did you do this week
- Considered converting the Flask app to a desktop app instead.
- Searching and testing new LLM (Ollama, Llama 3, 4.7Gb model) to try to replace existing openAI then checking CPU usage and its response speed.
- Considered what issues I can indentify for CertIV students to contribute. 
>What work you are planning to do next week
- Finding out any ways to improve performance in CPU usage and response time.
- Searching for how to apply multiple OCRs to identify code frame and add timestamps, and with other OCR to extract and convert text to code.

> Any blockers
- Unexpected slow response speed of Llama 3 model and fairly high CPU usage
- Recognition accuracy of detecting differences in code 




#### Issues and PRs
> N/A

#### Evidence
Mark all that applied this week
- [V] Attended class
- [] Responded to PRs/Issues
- [V] Met with the team online. Forum Microsoft Teams
- [] Commits to group repo

> warning: If you were not able to mark any of these on a particular week, please email your lecturer with the reason.

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?
- Personally think that using various of Ollama models could be more beneficial in pricing and performance rather than training our own LLM or relying on GPT 3.5.   
> Did you discuss these ideas with the group? What was the outcome?
- I need more time to test more models and to see if it can be more useful and replaceable in actual use.     
> How did you validate your progress this week?
- I've downloaded some models of Ollama and tested them on my PC.


