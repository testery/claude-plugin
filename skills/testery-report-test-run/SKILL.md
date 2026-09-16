---
name: testery-report-test-run
description: Output per-test results for a completed Testery run as a pretty pass/fail summary with emojis. Use when the user asks for results, a status report, or wants to see which tests passed/failed.
---

# Report a Testery test run

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery report-test-run`, then renders a human-friendly summary with status emojis.

## What the CLI actually returns

`report-test-run` reports at the **run level** (totals + status), not a per-test list:

- **Default** (no `--output`): prints a single line, e.g. `Completed: 33 of 34 pass with 1 fail`.
- `--output json`: prints the run object (Python-dict style — single quotes, `True`/`False`), which includes `status`, `totalCount`, `passCount`, `failCount`, `ignoredCount`, `notRunCount`, `timeoutCount`, `startTime`, `endTime`, etc.
- `--output sonarcube`: SonarQube-format output (the only named format the help documents).
- `--outfile <path>`: write the output to a file instead of stdout.
- `--fail-on-failure`: exit non-zero when there are test failures.

> For a per-test breakdown (individual scenario pass/fail with errors), the CLI does not provide it here — use the Testery MCP `get_test_results` tool, or read the run from `testery list-test-runs --output json`.

## Status legend

- ✅ passed
- ❌ failed
- ⏭️ skipped / pending / ignored
- 🟡 running / in-progress
- ⚠️ errored / unknown

## Rendering: inline widget vs. text

Before rendering the totals summary or per-test breakdown, check once per session whether inline widget rendering is available:

- Look for a `show_widget` tool from a `visualize` MCP server (it may appear as `visualize:show_widget`, `mcp__visualize__show_widget`, or similar). If your harness supports deferred-tool discovery, do one search for it (e.g. `select:mcp__visualize__show_widget`) — don't repeat the search on later calls in the same session.
- **If found:** build a small, self-contained HTML snippet — totals, a status pill (✅/❌/⚠️), and one row per test with the same ✅/❌/⏭️/🟡/⚠️ semantics as below — and pass it to `show_widget` to render inline. No external scripts/styles/fonts *except* the Testery logo image below; the widget sandboxes content. If the call errors, don't retry it for the rest of the session — fall back to text for the remainder.

  Include, above the totals:
  - **Logo:** the Testery wordmark, embedded as a self-contained data URI so it renders inside the widget sandbox (external hosts other than the CDN allowlist are blocked by CSP). Emit it verbatim:

    ```html
    <img src="data:image/png;base64,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" alt="Testery" style="height:28px">
    ```

    It's a dark/black wordmark, so wrap it in a container with an explicit light/white background (e.g. `background:#fff; padding:8px 12px; border-radius:6px;`) so it stays legible regardless of the surrounding theme — don't rely on the page background.
  - **Pass/fail pie chart:** a CSS `conic-gradient` circle (no chart library needed) sized ~120px, one segment per status present (passed/failed/ignored+notRun+timeout grouped as "skipped"), plus a small legend with counts and percentages. Compute each segment's degrees from its share of `totalCount` (360° × share), stacking cumulatively. Colors: passed `#22c55e`, failed `#ef4444`, skipped `#9ca3af`. Example for 33 passed / 1 failed / 0 skipped out of 34 (97.06% / 2.94%):
    ```html
    <div style="width:120px;height:120px;border-radius:50%;
         background:conic-gradient(#22c55e 0deg 349.4deg, #ef4444 349.4deg 360deg);"></div>
    ```
    If every test is the same status (0% or 100% split), render a solid circle in that status's color rather than a degenerate gradient.
  - **Status filter pills:** directly above the per-test list, a row of pills — `All <total>`, `Passed <n>`, `Failed <n>`, plus `Skipped <n>` only when that count is non-zero — that filter the list client-side. Wire them up in the trailing `<script>` (it runs after streaming completes): toggle each test row's `display`, hide any feature-file group left with no visible rows, update a live `Showing <x> of <total>` count in an `aria-live="polite"` element, and set `aria-pressed` on each pill. Do the filtering in JS — never round-trip through `sendPrompt` for it. Default to `All` so nothing is hidden while the widget streams, and show a "No tests match this filter." line if a pill ever yields an empty list. Style the active pill with `background:var(--bg-accent); color:var(--text-accent); border-color:var(--border-accent)` and leave the inactive ones transparent with `var(--border-strong)`.
  - **Links back to Testery:** make the widget clickable. The run title and a `View results` action link to the run page; every test row links to its own result (`.../tests/<testId>`); a failed test additionally gets `Console & video` (`.../tests/<testId>/console`); and an action row carries `Rerun tests` (the run page — see below) and `All runs` (`/test-runs`). Plain `<a href="https://...">` is enough — the host intercepts the click and shows its own link-confirmation dialog. Only emit a per-test link when you hold a real `<testId>` from the results API; never synthesize or extrapolate one.
- **If not found** (e.g. running in Claude Code CLI / VS Code, where this app isn't exposed), or the widget call fails: use the text-based formatting below. This is the default, always-available path — don't ask the user to choose, and don't block waiting on this check.

## Steps

1. Fetch the run-level result as JSON:
   ```bash
   TESTERY_SKILL="testery-report-test-run" testery report-test-run \
     --token "$TESTERY_TOKEN" \
     --test-run-id <id> \
     --output json \
     --outfile /tmp/testery-run-<id>.json
   ```
   (Note: the file is Python-dict style, not strict JSON — normalize `'`→`"`, `True`→`true`, `False`→`false` before parsing, or just read the fields directly.)

2. Render a totals summary (inline widget if available, else text — see "Rendering" above). Include the run URL on the header line (see "Testery URLs" below):

   ```
   Testery Test Run <id>  ·  <project> @ <env>
   https://testery.app/<accountName>/test-runs/<runId>
   ─────────────────────────────────────────────
   Total: 34   ✅ 33   ❌ 1   ⏭️ 0     Duration: 7m43s
   Status: ❌ FAILED
   ```

   Map `status` to a verdict emoji: `PASS`/`PASSED` → ✅, `FAIL`/`FAILED` → ❌, `RUNNING`/`IN_PROGRESS`/`QUEUED` → 🟡, anything else → ⚠️ (include the raw status).

3. **For a per-test breakdown** (when the user wants individual scenarios), pull results from the Testery MCP `get_test_results` and render one line per test (inline widget if available, else text). Link each failing test to its console page:

   ```
   ✅ login.feature › User logs in successfully           1.2s
   ❌ checkout.feature › User completes checkout          3.4s
       → AssertionError: expected "Order placed" got "Error"
       → https://testery.app/<accountName>/test-runs/<runId>/tests/<testId>/console
   ⏭️ profile.feature › Avatar upload (skipped: @wip)
   ```

   For failed tests, include the error/stack snippet beneath the line (indented `    →`; truncate long stacks to ~5 lines) and a link to its console page.

## Testery URLs

Testery app URLs follow `https://testery.app/<accountName>/<page>`.

Resolve `<accountName>`, once per session, in this order:

1. `$TESTERY_ACCOUNT_SLUG`, if set.
2. `GET https://api.testery.io/api/account` with the API token — the `name` field is the slug used in app URLs. (Dev: `https://api.dev.testery.io/api`.)
3. Otherwise emit the `<accountName>` placeholder and ask the user to set `TESTERY_ACCOUNT_SLUG`.

Route patterns, as defined by the web app's router:

- Run results: `https://testery.app/<accountName>/test-runs/<runId>`
- A tab on that page: `.../test-runs/<runId>/<tab>` — valid tabs are `analysis`, `chat`, `code`, `details`, `history`, `info`, `logs`, `messages`, `test-results`, `test-selection`, `timeline`.
- A single test: `.../test-runs/<runId>/tests/<testId>`
- That test's console (logs/screenshots/video; use for failures): `.../test-runs/<runId>/tests/<testId>/console`
- All runs: `https://testery.app/<accountName>/test-runs`

**Getting `<testId>`:** `report-test-run` never emits test IDs — `--output` writes SonarQube XML whatever value you pass it. Fetch them from `GET https://api.testery.io/api/test-runs/<runId>/results`, which returns one object per test carrying `id` (the `<testId>`), `status`, `duration`, and `projectTest.name`.

**Rerun is an action, not a URL.** The app reruns via `POST /api/test-runs/<runId>/rerun`; no GET route triggers one, and the widget sandbox is unauthenticated. A `Rerun tests` control must therefore link to the run page, where the app's own rerun buttons live. Do not link to `/test-runs/<runId>/rerun` — there is no such tab, and it silently lands on the results page.

## CI use

For a non-interactive check, pass `--fail-on-failure` so the CLI itself exits non-zero on failures:

```bash
TESTERY_SKILL="testery-report-test-run" testery report-test-run --token "$TESTERY_TOKEN" --test-run-id <id> --fail-on-failure
```
