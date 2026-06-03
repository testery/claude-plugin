---
description: Implement application code to make a failing playwright-bdd scenario pass (changes app code, not the test).
---

Use the `testery-playwright-bdd-implement-code` skill.

If `$ARGUMENTS` names a specific scenario, target that one. Otherwise default to the most recently failing scenario (typically the one just added via `/bdd-add-scenario`).

Default to modifying **application code** to satisfy the scenario. Step definitions may be edited only when needed for testability (e.g. add a `data-testid` in the app and switch the step's locator to use it). Never edit the `.feature` text or weaken assertions. After each change, re-run just that scenario via `testery-playwright-bdd-run-local --grep "<scenario>"` until it passes. Then tell the user it's green and suggest running the full suite.

User input (optional: scenario name): $ARGUMENTS
