---
name: testery-playwright-bdd-view-report
description: Open the Playwright HTML report for the most recent local test run in a browser. Use when the user asks to "view the report", "see test results", "open the playwright report", or runs `/bdd-view-report`.
---

# View the Playwright HTML report

Playwright writes the HTML report to `playwright-report/` (configurable via the `reporter: "html"` line in `playwright.config.ts`). `npx playwright show-report` serves that directory on a local port and opens the user's default browser automatically.

## Steps

1. Detect the report directory (in order):
   - `./playwright-report/`
   - if not found, look for a single `playwright.config.*` and resolve relative to it
   - if still not found, tell the user to run the suite first via `/bdd-test` and stop.
2. Open the report:
   ```bash
   npx playwright show-report
   ```
   This starts a local server (default `http://localhost:9323`) and auto-opens the user's default browser. Pass an explicit path if the report lives elsewhere: `npx playwright show-report path/to/playwright-report`.
3. The command runs in the foreground until the user stops it (Ctrl+C). Run it via Bash with `run_in_background: true` so the conversation isn't blocked, then surface the URL it printed (typically `http://localhost:9323`) so the user can revisit the tab.
4. If the browser doesn't open automatically (e.g. headless WSL, SSH session), print the URL and tell the user to open it manually.

## Notes

- `show-report` honors any `reporter` settings in `playwright.config.ts`, so a customized output dir works as long as it's named on the command line.
- The HTML report is regenerated each time `playwright test` runs; there's no cache to clear.
