# Overview

As part of the project, you and your team are required to evidence that you have **designed** an advanced user interface that is fit for purpose.

The following guide will help you ensure that you have met the evidencing requirements while ensuring that you can work in an agile/iterative way that is appropriate for the project and modern software development practices.

## Design Evidencing

Modern design approaches are lightweight and combine iterations with user feedback. This is in contrast to traditional design approaches that are heavy on documentation and require a lot of up-front work.

However, often we cannot access the user in the frequency that allows rapid iteration. One way to mitigate this is to develop personas and scenarios that represent the user and their goals. This allows you to make design decisions based on the user's needs and goals.

### Minimum Requirements

1. In your project repository, create a folder called `design`.
2. In the `design` folder, create a file called `persona.md` that describes the key persona your team was focused on implementing the design (see below for detail)
3. Create a subfolder with any design artefacts you created: wireframes, sketches, mockups, etc.
4. If you are treating the application itself as a prototype, highlight what changes if any you made to the application by referencing the appropriate issues
5. Create at least three github issues related to the design of the application:
   1. Tag each issue with ui-design
   2. Assign each issue to a team member
   3. Include a user story in the format "As a [persona], I want to [goal], so that [reason]"
   4. Add any non-functional requirements as notes in the issue
6. Copy this document into your project and answer any relevant questions

## Personas

A persona is a fictional character that represents a user. It is a way to describe the user's goals, needs, and behaviors. They are focused on **empathy** and **understanding** the user, not demographics, and not a collection of features.

> Describe the key persona your team was focused on implementing the design. You can describe the persona in a file called `persona.md` in the `design` folder.
>

Pick the most representative persona from your group. Write a brief (2-3 sentence) justification for why you chose this persona.

### Chosen persona
[Steve](persona.md)

### Relevant issue
>
> 1. [Create Media Player with Timestamps #10](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/10)
> 2. [Media Player Timestamp Alert #36](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/36)
> 3. [Block out UI #4](https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-facilitate/issues/4)
>

### Validation

You will validate your design by meeting with a user representative: the product owner (in this case, your lecturer).

##### Meeting minutes

- [x] Meeting held on 11/06/2024
- [x] Persona discussed: Steve
- [x] Design artefacts reviewed: app-flow.jpg and find-text-occurrence.jpg
- [x] Issues discussed
- [x] Feedback provided

##### What worked well

- Use of low fidelity mock-ups
- Understood persona, allowing us to prioritise the core components of the project

##### What could be improved

- A lot of focus on technical detail over app flow
- Needed better understanding of how code follows video
- Mismatch of transcript presentation across team members

##### What will you change before the next meeting

- User test assumptions 
- Validate framing of transcript presentation with user, whether a live representation of 
  code on screen is preferable to a pre-generated transcript displaying all code occurrences
- Test code generation matches expectations

##### Were there any questions that needed to be discussed with the user

- Yes, we needed to discuss user preference for display of the code transcript

#### Lecturer's checklist (to be used by the lecturer)

- [ ] Persona is well-defined
- [ ] Persona is relevant to the application
- [ ] Design artifacts are present and easy to follow
- [ ] Design decisions are based on user needs and goals
- [ ] Appropriate considerations of interaction patterns appropriate for the user
- [ ] Efforts towards realizing at least one significant issue involving user interaction
- [ ] Whole team engagement in the design process
