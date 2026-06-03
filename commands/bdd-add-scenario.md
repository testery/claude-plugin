---
description: Add a new Scenario to a playwright-bdd project, implement missing step defs, run just that scenario, and walk the user through the red→green loop.
---

Use the `testery-playwright-bdd-add-scenario` skill.

If `$ARGUMENTS` is empty, run interactively: prompt for the scenario name, target feature file (or new), steps (one per line, blank to finish), and optional tags. Otherwise treat `$ARGUMENTS` as the scenario name.

After writing the scenario:
1. Run `npx bddgen` and implement any missing step definitions in the appropriate `tests/steps/*.steps.ts` file (do NOT delegate; implement them as part of this flow).
2. Run only the new scenario locally via the `testery-playwright-bdd-run-local` skill (`--grep "<scenario-name>"`).
3. If it fails (expected), tell the user: **"Run `/bdd-implement-code` to implement the app code so this passes."**
4. After they run `/bdd-implement-code`, re-run just this scenario. Iterate until green.
5. When green, ask whether to run the full suite.

User input: $ARGUMENTS
