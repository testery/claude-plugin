---
name: testery-playwright-bdd-add-step-definition
description: Add a Given/When/Then step definition to a playwright-bdd project. Use when scenarios reference an undefined step.
---

# Add a step definition

## Steps

1. Locate the right `tests/steps/<area>.steps.ts` file (one per page/area, e.g. `navigation.steps.ts`, `commerce.steps.ts`). Create a new `*.steps.ts` only if no existing file fits.
2. Surface the undefined step by regenerating tests:
   ```bash
   npx bddgen
   ```
   The output names any steps without a matching definition.
3. Implement the step. Conventions in this project:
   - Imports: `import { createBdd } from 'playwright-bdd'` and `import { expect } from '@playwright/test'`. If the project has `tests/steps/fixtures.ts`, prefer `import { Given, When, Then } from './fixtures'` so custom fixtures are available.
   - Handler signature: `async ({ page }, ...args) => { ... }` (Playwright fixtures destructured from the first arg, not `this`).
   - Quoted/numeric args use cucumber expressions: `{string}`, `{int}`, etc.
   - Drive the page via `page.getByRole`, `page.getByLabel`, etc. If the project uses page objects, prefer those over raw locators.
4. Re-run `npx bddgen`; the step should now resolve. Then run the suite via `testery-playwright-bdd-run-local`.

## Skeleton

```ts
import { expect } from '@playwright/test';
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

When('I click the {string} menu item', async ({ page }, label: string) => {
  await page.getByRole('button', { name: label }).click();
});

Then('I should see the {string} heading', async ({ page }, text: string) => {
  await expect(page.getByRole('heading', { name: text })).toBeVisible();
});
```

If the project has `tests/steps/fixtures.ts`, swap the import:

```ts
import { Given, When, Then } from './fixtures';
```
