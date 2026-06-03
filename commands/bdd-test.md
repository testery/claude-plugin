---
description: Run the local playwright-bdd test suite, optionally filtered to a single scenario by name.
---

Use the `testery-playwright-bdd-run-local` skill.

If `$ARGUMENTS` is non-empty, treat it as a scenario name (or partial name / regex) and run `npx bddgen && npx playwright test --grep "$ARGUMENTS"` so only that scenario runs. If empty, run the full suite (`npm run test:e2e`).

User input (optional: scenario name to filter): $ARGUMENTS
