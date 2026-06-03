---
name: testery-playwright-bdd-implement-code
description: Implement (or modify) the actual application code so a failing playwright-bdd scenario passes. Use when the user runs `/bdd-implement-code`, or asks to "make the test pass", "implement the feature behind this scenario", or "fix the failing test by changing the app code (not the test)".
---

# Implement application code to satisfy a failing scenario

This is the second half of the BDD loop. The first half (`/bdd-add-scenario`) wrote a Gherkin scenario, generated step definitions, and ran the scenario, producing a *failing* test. This skill changes the **application code** (NOT the test) so the scenario passes.

## Operating principles

- **Default to changing app code.** The scenario and step definitions describe desired behavior; the app should satisfy them. Implementing the feature in app code is the goal of this skill.
- **Modify tests only for testability, not to dodge the assertion.** It's fine to:
  - Add a `data-testid` (or accessible name/role) in the app *and* update a step definition's locator to use it.
  - Adjust a step's locator strategy if the app's intended UI doesn't match what the step assumes (e.g. switch from `getByText` to `getByRole` after wiring proper semantics).
  - Tweak a step's wait/timeout when the app legitimately needs async settling.

  Don't change the `Scenario:` text or weaken an `expect(...)` to make a red test green. If the scenario itself is wrong, stop and ask the user.
- **Smallest diff that turns the test green.** No speculative refactors, no unrelated cleanups.
- **Stay inside the app's existing patterns.** Match the framework, file structure, and style of neighboring code (read it before writing).

## Steps

1. **Locate the failing scenario.** Prefer the scenario the user just added via `/bdd-add-scenario`. If unclear, ask: "Which scenario should pass?" (or run the suite and pick the first failure).

2. **Reproduce the failure.** Run just that scenario via the `testery-playwright-bdd-run-local` skill (`--grep "<scenario-name>"`). Capture the assertion message, the failing locator, and any HTML/screenshot from `test-results/`. Don't guess at the cause.

3. **Map test expectations → code changes.**
   - Identify which app surface the test is poking: a route, a page component, an API endpoint, a piece of business logic.
   - For UI scenarios in projects shaped like `example-webapp/web/`, the app code lives in `web/src/` (React components, routes, etc.). For backend scenarios, look at `api/app/` (or equivalent).
   - For each `expect(...)` in the failing step definitions, identify the source of truth in the app and what needs to change.

4. **Implement the change.** Edit existing files when possible; create new ones only when adding genuinely new surface (e.g. a new route/page/component the test references). Keep the change minimal and self-contained.

5. **Re-run the scenario.** Hand back to the `testery-playwright-bdd-run-local` skill with `--grep "<scenario-name>"`. If still failing:
   - Read the new failure carefully — it's often a different problem than the first.
   - Iterate on the app code, not the test.
   - If after a couple of iterations the test seems to be asserting something the app shouldn't reasonably do, stop and ask the user whether the scenario is actually right.

6. **Confirm green.** Once the targeted scenario passes, tell the user. Suggest they go back to `/bdd-add-scenario` (which will offer to run the full suite) or run `/bdd-test` themselves.

## What this skill does NOT do

- It does not edit `tests/features/*.feature` (the scenario text). Those are owned by `/bdd-add-scenario`.
- Step definitions in `tests/steps/*.steps.ts` may be touched *only* for testability (locator/wait adjustments), never to weaken or skip assertions.
- It does not register Testery projects, kick off cloud runs, or change CI config.
- It does not run lint/format unless asked: it changes the smallest set of files needed to flip red → green.
