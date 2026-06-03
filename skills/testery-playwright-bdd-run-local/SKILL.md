---
name: testery-playwright-bdd-run-local
description: Run playwright-bdd tests locally on the current developer machine. Use when the user asks to "run the tests", "run the e2e tests", or "run locally".
---

# Run playwright-bdd tests locally

Playwright-bdd is a two-step pipeline: `bddgen` compiles `.feature` + `*.steps.ts` files into Playwright test files, then `playwright test` runs them. The standard `package.json` wires both together.

## Whole suite

```bash
npm run test:e2e
```

(equivalent to `bddgen && playwright test`, configured via `defineBddConfig` in `playwright.config.ts`)

## A single feature

```bash
npx bddgen && npx playwright test tests/features/<file>.feature
```

`playwright test` accepts the original `.feature` path; playwright-bdd maps it to the generated test.

## A subset by tag

```bash
npx bddgen && npx playwright test --grep "@smoke"
```

(Tags from `.feature` files are propagated into Playwright's test titles, so `--grep` matches them.)

## A single scenario by name

```bash
npx bddgen && npx playwright test --grep "<scenario-name>"
```

The scenario's `Scenario:` text becomes the Playwright test title, so `--grep` matches by substring or regex. Use this when running just the scenario you're iterating on (e.g., during the `/bdd-add-scenario` red→green loop).

## Generate only (no execution; surfaces undefined steps)

```bash
npx bddgen
```

## Steps

1. Confirm the project has `playwright.config.ts` with `defineBddConfig({ features, steps })` and `package.json` has `playwright-bdd` in `devDependencies`. Most projects expose a `test:e2e` script.
2. If Playwright browsers aren't installed yet: `npx playwright install chromium` (one-time).
3. Pick whole-suite, single-feature, or tag-filtered. Run the command.
4. Reports land in `playwright-report/` (HTML) and `test-results/` (artifacts), per `playwright.config.ts`. Open the HTML report with `npx playwright show-report`.
