# Reflection

This project reinforced that AI-assisted coding is most useful when the work is kept small, constrained, and verifiable. The strongest part of my process was separating each feature into backend rules, tests, and frontend integration instead of asking the AI to rewrite the whole Task Tracker. That made the generated changes easier to inspect and reduced the chance of accepting unrelated code.

One moment where AI helped was the due-date feature. It quickly produced a clean model change and a reusable overdue helper. However, the first version treated every past due date as overdue. I reviewed the business meaning and corrected the rule so completed tasks are not overdue. That was a useful reminder that plausible code is not the same as correct business logic.

A second important moment came with tags. AI suggested validation, but its initial approach did not fully handle duplicates with different capitalization. I refined the requirement and changed the validator to trim values, reject blanks, and de-duplicate tags case-insensitively.

The Break Tests were especially valuable. Temporarily disabling status-transition validation showed that the related pytest test failed for the intended reason, which increased confidence that the test was protecting behavior rather than merely exercising a route. The same idea was used for blank-tag validation.

If I repeated this sprint, I would keep the same narrow prompt style and spend even more time defining acceptance criteria before generating code. I would also record the exact baseline test count and manual browser evidence before the first modification. Overall, the project showed me that AI works best as a junior collaborator: it can draft quickly, but I still need to inspect, test, constrain, and take responsibility for the final result.
