## <22/May>

#### Summary

> What work did you do this week

- Organised and led a team meeting to determine requirements for our app and discuss key
  user stories
- Worked with everyone to choose the direction we would like to take our app: A native
  videoplayer that can extract all code occurrences in a video and have a transcript
  available to the user before the video has begun.

> What work you are planning to do next week

- Establish some issues and assign project members
- Draft an app flow wireframe that focuses on two areas:
    - user experience, the steps they take to interact with the app and the functionality
      available to them
    - programmatic flow, what the key components for our solution will be, how they interact
      and communicate with each other
- Hold another meeting to collaboratively build diagram and have discussion

> Any blockers

- While we would like to develop a solution that is decoupled from openAI, it looks
  difficult for our purposes
- I am unfamiliar with many of the libraries we will be using in this project

#### Issues and PRs

> N/A

#### Evidence

Mark all that applied this week

- [X] Attended class
- [X] Responded to PRs/Issues
- [X] Met with the team online. Forum Microsoft Teams
- [] Commits to group repo

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?

- Our intended design to automatically scan the entire frame of a video requires something
  like chatGPT to format and identify the text correctly, as much as I'd like to come up
  with another solution, without manual input from a user I don't think it'd be easily
  doable in our timeframe.

> Did you discuss these ideas with the group? What was the outcome?

- All discussion has been collaborative, we decided to go ahead with the solution proposed
  above.
- Alexander decided to look into researching LLMs and seeing if there would be any potential
  application in our project.

> How did you validate your progress this week?

- Discussion with team leader

## <4/June>

#### Summary

> What work did you do this week

- Worked with the team to produce the app flow diagram
- Onboarded the CERT IVs to the project, introducing them to our project and goal, sharing
  the minutes from our previous meetings, and established guidelines on how they can
  contribute. Informing them that issues tagged with `good first issue` are marked as such
  for the CERT IVs.

> What work you are planning to do next week

- Organise validation meeting with project director

> Any blockers

- To best facilitate simultaneous development, dummy data needs to be created for testing
  and validating design of each component.

#### Issues and PRs

> Created the following
> issue: [#8](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/8)

#### Evidence

Mark all that applied this week

- [X] Attended class
- [X] Responded to PRs/Issues
- [X] Met with the team online. Forum Microsoft Teams
- [] Commits to group repo

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?

- We were initially unsure about keeping the project as a flask application or refactoring
  it to native, but we committed fully to native when Alexander built a prototype UI with wx.

> Did you discuss these ideas with the group? What was the outcome?

- We all agreed upon marking specific issues for the CERT IVs, Alexander and I agreed to
  dedicate time to identifying issues for the CERT IVs.

> How did you validate your progress this week?

- Alexander and I set a target number of issues to create.

## <11/June>

#### Summary

> What work did you do this week

- Initiated validation meeting with project director
- Generally led the discussion, answering questions, and explained the progress of our project

> What work you are planning to do next week

- Implement feedback from meeting, particularly on testing assumptions and choosing the
  right method to display the transcript

> Any blockers

- Time constraints, meeting deadlines for not only this class but other clusters as well.

#### Issues and PRs

> Created the following issues:
> [#36](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/36)
> [#39](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/39)
> [#40](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/40)
> [#43](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/43)
> Submitted the following pull
> request: [#17](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/pull/17)

#### Evidence

Mark all that applied this week

- [X] Attended class
- [X] Responded to PRs/Issues
- [X] Met with the team online. Forum Microsoft Teams
- [X] Commits to group repo

#### Retrospective

> In what ways have your thoughts about the design changed this week and why?

- My idea for how the transcript would appear in the media player was not one shared by the
  rest of the team, as I had imagined a "historical view" that displays occurrence of code
  within a video at all times, that would serve as points to navigate to in the video.
  Whereas Bianca had imagined and implemented a live view system instead, filling with the
  currently displayed code, as it appeared in the video.

> Did you discuss these ideas with the group? What was the outcome?

- We intend to create prototypes for both of our solutions and determine which works better
  and overall suits the project best

> How did you validate your progress this week?

- Validation meeting with project director and conversation with team leader
