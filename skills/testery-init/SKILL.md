---
name: testery-init
description: Bootstrap a project with playwright-bdd tests AND wire it up to Testery in one shot. Scaffolds files, installs deps, registers a Testery project + environment, runs a local smoke test, then optionally fires the first run on Testery. Use when the user says "set up Testery here", "add playwright-bdd to this project", "init Testery", or starts in an empty repo.
---

# Initialize Testery + playwright-bdd in a project

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

End state: working playwright-bdd suite locally, a Testery project + environment registered, and the first green run on Testery (optional).

The archetype is `example-webapp/web/`.

## Pre-flight

1. **Auth.** If `TESTERY_TOKEN` isn't valid, hand off to the `testery-onboard` skill first.
2. **Git status.** Note whether the cwd is a git repo. If not, ask whether to `git init`. (Optional: Testery doesn't require it for `--build-id` flows, but `--git-branch` flows do.)
3. **Existing setup detection.** Look for an existing `playwright.config.ts` that calls `defineBddConfig`, or `package.json` with `playwright-bdd` + `@playwright/test` deps. If present, skip scaffolding and jump to the Testery registration step.

## Scaffold (skip files that already exist)

Mirror the `example-webapp/web/` layout. Create:

### `package.json`
```json
{
  "name": "<project-folder-name>",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "bdd": "bddgen",
    "test:e2e": "bddgen && playwright test"
  },
  "devDependencies": {
    "@playwright/test": "^1.47.0",
    "playwright-bdd": "^7.3.0",
    "typescript": "^5.5.0"
  }
}
```

### `playwright.config.ts`
```ts
import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const testDir = defineBddConfig({
  features: "tests/features/**/*.feature",
  steps: "tests/steps/**/*.ts",
});

export default defineConfig({
  testDir,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],
});
```

### `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "types": ["node"]
  }
}
```

### `tests/features/sample.feature`
```gherkin
Feature: Sample navigation

  @smoke
  Scenario: User loads the Testery site
    When I navigate to "https://www.testery.io"
    Then the page title contains "Testery"
```

### `tests/steps/navigation.steps.ts`
```ts
import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { When, Then } = createBdd();

When("I navigate to {string}", async ({ page }, url: string) => {
  await page.goto(url);
});

Then("the page title contains {string}", async ({ page }, expected: string) => {
  await expect(page).toHaveTitle(new RegExp(expected));
});
```

### `.gitignore` (append, don't overwrite)
```
node_modules/
playwright-report/
test-results/
.features-gen/
.testery/
```

### `testery.yml` (project-level Testery config Testery will pick up)
```yaml
framework: playwright-bdd
testCommand: npm run test:e2e
```

## Install + smoke

```bash
npm install
npx playwright install chromium
npm run test:e2e
```

Render the local result with the same emoji format used by `testery-report-test-run` (✅ ❌ ⏭️). If the smoke fails, stop and help the user before doing any Testery wiring.

## Register on Testery

Ask the user for:
- **Project key** (default: kebab-cased folder name)
- **Project name** (default: titlecased folder name)
- **First environment key + name** (default: `dev` / `Dev`)
- (Optional) URL of the app under test → set as a `BASE_URL` variable

Then:

1. **Project**: Testery has no `create-project` CLI command, so use the REST API directly:
   ```bash
   curl -fsS -X POST "https://api.testery.io/projects" \
     -H "Authorization: Bearer $TESTERY_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key":"<project-key>","name":"<project-name>","framework":"PLAYWRIGHT"}'
   ```
   Capture the response (id) for confirmation. If the project already exists, that's fine: continue.

2. **Environment**: use the CLI:
   ```bash
   TESTERY_SKILL="testery-init" testery create-environment \
     --token "$TESTERY_TOKEN" \
     --key "<env-key>" \
     --name "<env-name>" \
     [--variable "BASE_URL=<url>"]
   ```

## First run on Testery (optional, ask)

Two options: ask the user which:

- **Local working copy** (no git push needed): hand off to the `testery-playwright-bdd-run-on-testery-local-build` skill (zips with proper excludes, uploads, runs).
- **From Git** (requires the repo to be pushed and connected to Testery):
  ```bash
  TESTERY_SKILL="testery-init" testery create-test-run --token "$TESTERY_TOKEN" --project-key "<project-key>" --environment-key "<env-key>" --git-branch "$(git rev-parse --abbrev-ref HEAD)" --wait-for-results --output json
  ```

Pipe results through the emoji renderer from `testery-report-test-run`.

## Wrap-up

Print a short "what's next" list:
- `/bdd-add-scenario` to add more tests (drives the red→green loop)
- `/bdd-implement-code` to implement app code that satisfies a failing scenario
- `/bdd-test` to run the suite locally; `/bdd-view-report` to open the HTML report
- `/testery-create-schedule` to run on a cron / on deploy
- `/testery-monitor-test-run <id>` to watch a run
- The Testery web app for dashboards & alerts

## Idempotency

The skill should be safe to re-run: every step checks for prior existence (files, project, environment) and skips/upserts rather than failing.
