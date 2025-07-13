Quality Attributes for the Anki Deck Generator Project
1. Usability
Importance to the Customer:
The tool must be intuitive and easy to use, as the target audience includes language learners who may not be tech-savvy. A clear interface and straightforward workflow are critical for user adoption.

Quality Attribute Scenarios:

Scenario 1: A user uploads a text, marks unfamiliar words, and generates a deck without errors.

Test: Manual testing by following the user journey and verifying each step.

Scenario 2: Instructions are clear, and users can navigate between modes (beginner/advanced) effortlessly.

Test: User testing with feedback on clarity and ease of navigation.

2. Performance Efficiency
Importance to the Customer:
The tool should process texts and generate decks quickly to avoid frustrating delays, especially when handling large texts or frequent updates.

Quality Attribute Scenarios:

Scenario 1: The system processes a 1000-word text and generates a deck in under 10 seconds.

Test: Measure processing time with a sample text and verify against the threshold.

Scenario 2: The OpenAI API responds within 3 seconds for translation and example generation.

Test: Automated API response time tracking during CI pipeline runs.

3. Maintainability
Importance to the Customer:
As the project evolves, the codebase should remain easy to update and extend, especially for adding new language supports or features.

Quality Attribute Scenarios:

Scenario 1: A new developer can add support for German language within 2 hours by following documented steps.

Test: Assign the task to a new team member and track completion time.

Scenario 2: Static analysis tools report zero critical code smells in the CI pipeline.

Test: Integrate SonarQube or similar tools and enforce zero-tolerance for critical issues.


