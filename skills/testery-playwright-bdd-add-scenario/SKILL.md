---
name: testery-playwright-bdd-add-scenario
description: Add a new Scenario (or Feature) to a playwright-bdd project, implement any missing step definitions, run just that scenario, and walk the user through the red→green loop with /bdd-implement-code. Use when the user asks to "add a test", "add a scenario", or "add a feature" in a project shaped like example-webapp/web.
---

# Add a playwright-bdd scenario (and drive the red→green loop)

Project shape (mirrors `example-webapp/web/`):

- Features: `tests/features/*.feature`
- Step defs: `tests/steps/*.steps.ts` (one per page/area)
- Fixtures: `tests/steps/fixtures.ts` re-exports `Given/When/Then` from `createBdd(test)`
- Config: `playwright.config.ts` calls `defineBddConfig({ features, steps })`; tests run via `bddgen && playwright test` (typically `npm run test:e2e`)

## Steps

1. **Gather inputs.** If the user invoked the skill without arguments (or args don't include a scenario name), prompt interactively:
   1. Ask: **"What's the scenario name?"** (a single human-readable line, e.g. *"User can delete an employee"*). Don't proceed without one.
   2. Ask: **"Which feature file should it go in?"** Default to the closest topical match in `tests/features/` (show the candidates). Offer `<new>` to create a new feature file; if chosen, ask for the new feature filename and `Feature:` heading.
   3. Ask: **"Enter the steps, one per line (Given/When/Then/And). Blank line to finish."** Collect them in order. Validate each line starts with `Given`, `When`, `Then`, `And`, or `But`. If the user just hits enter immediately, prompt again with an example.
   4. Ask: **"Any tags? (e.g. `@smoke`, blank for none)"**.

   If the user passed arguments to the slash command, parse them as the scenario name (and optional feature name / tags) and skip the corresponding prompts.

2. **Write the scenario.** Determine whether it fits an existing `.feature` (same Feature heading) or needs a new file. **Existing**: append a `Scenario:` block, matching the project's tag conventions and keeping `Given/When/Then` phrasing close to existing steps in the file so step definitions can be reused. **New**: create `tests/features/<name>.feature` with a `Feature:` heading and the `Scenario:` block.

3. **Find undefined steps.** Run `npx bddgen` to generate test files and surface any steps without a matching definition.

4. **Implement missing step definitions.** For each undefined step:
   - Locate the right `tests/steps/<area>.steps.ts` (one per page/area, e.g. `navigation.steps.ts`). Create a new `*.steps.ts` only if no existing file fits.
   - Imports: `import { createBdd } from 'playwright-bdd'` and `import { expect } from '@playwright/test'`. If the project has `tests/steps/fixtures.ts`, prefer `import { Given, When, Then } from './fixtures'`.
   - Handler signature: `async ({ page }, ...args) => { ... }`. Quoted/numeric args use cucumber expressions (`{string}`, `{int}`, etc.).
   - Drive the page via `page.getByRole`, `page.getByLabel`, etc. If the project uses page objects, prefer those; otherwise drive `page` directly (the example-webapp/web archetype does this).
   - Re-run `npx bddgen`; the step should now resolve.

   Skeleton:
   ```ts
   import { expect } from '@playwright/test';
   import { createBdd } from 'playwright-bdd';
   const { Given, When, Then } = createBdd();

   When('I click the {string} menu item', async ({ page }, label: string) => {
     await page.getByRole('button', { name: label }).click();
   });
   ```

5. **Run just this scenario.** Hand off to the `testery-playwright-bdd-run-local` skill, passing the scenario name so it runs `npx bddgen && npx playwright test --grep "<scenario-name>"`. Report the result.

6. **Red→green handoff.** The new scenario almost certainly fails (no app code yet). When it does:
   - Tell the user: **"This scenario is failing. Run `/bdd-implement-code` to make the app code satisfy it."**
   - After the user runs `/bdd-implement-code`, re-run *just this scenario* via the run-local skill (same `--grep`). Iterate until green.

7. **Offer the full suite.** Once the scenario is green, ask the user: **"This scenario passes. Run the full test suite to check for regressions?"** If yes, hand off to the run-local skill with no filter (full `npm run test:e2e`). If no, stop.

## Example block

```gherkin
@smoke
Scenario: User can navigate to the Employees page
  Given I am on the home page
  When I click the "Employees" menu item
  Then I should see the "Employees" heading
```
