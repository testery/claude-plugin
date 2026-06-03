---
name: testery-playwright-bdd-add-page-object
description: Create a new Playwright page object class in a playwright-bdd project. Use when adding tests for a page that has no existing page object.
---

# Add a page object

Page objects are optional in playwright-bdd projects: simple suites (like `example-webapp/web`) call `page.getByRole(...)` directly from steps. Reach for a page object when a single page accumulates multiple step definitions and shared selectors are starting to drift.

## Steps

1. Inspect existing classes in `tests/pages/` (or `tests/pageObjects/`) to match style. If no such directory exists, create `tests/pages/`.
2. Create `tests/pages/<Name>Page.ts`: one class per page, named `<Name>Page`, default-exported.
3. Expose intent-revealing methods (e.g. `loginAs(user)`, `submit()`) that wrap raw locator calls. Step definitions should not contain raw selectors once a page object exists.
4. Use the page object from steps by constructing it with the Playwright `page` fixture:
   ```ts
   import LoginPage from '../pages/LoginPage';
   When('I log in as {string}', async ({ page }, user: string) => {
     await new LoginPage(page).loginAs(user);
   });
   ```
   If you find yourself instantiating the same page object across many steps, promote it to a custom fixture in `tests/steps/fixtures.ts`.

## Skeleton

```ts
import { Page } from '@playwright/test';

export default class LoginPage {
  constructor(private page: Page) {}

  async loginAs(user: { username: string; password: string }) {
    await this.page.getByLabel('Username').fill(user.username);
    await this.page.getByLabel('Password').fill(user.password);
    await this.page.getByRole('button', { name: 'Sign in' }).click();
  }
}
```
