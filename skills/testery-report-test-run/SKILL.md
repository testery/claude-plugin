---
name: testery-report-test-run
description: Output per-test results for a completed Testery run as a pretty pass/fail summary with emojis. Use when the user asks for results, a status report, or wants to see which tests passed/failed.
---

# Report a Testery test run

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery report-test-run`, then renders a human-friendly summary with status emojis.

## What the CLI actually returns

`--output` accepts only `sonarcube` and `junit`; there is no `json` option on this command, and passing one fails with `Invalid value for '--output'`.

- **Default** (no `--output`): prints a single line, e.g. `Completed: 33 of 34 pass with 1 fail`.
- `--output junit --outfile <path>.xml`: JUnit XML with one `<testsuite>` per spec/feature file and one `<testcase>` per test, carrying `time` (seconds) and a `<failure>` or `<skipped>` child when the test didn't pass. Every suite has a `testery.url` property with the run page URL. It includes setup-phase tests, which the run's `totalCount` leaves out, so the XML can list more tests than the headline total; say so when the numbers differ.
- `--output sonarcube --outfile <path>`: SonarQube generic test execution format.
- `--fail-on-failure`: exit non-zero when there are test failures.

**Auth:** `--token` is optional. The CLI falls back to `~/.testery/credentials` (pick a profile with `--profile`) or `$TESTERY_API_TOKEN`, so omit `--token` unless the user gave you one.

**Run details** (`status`, counts, `startTime`/`endTime`, `branch`, `gitRef`, `excludedTags`) aren't in `report-test-run`'s output. Get them as strict JSON from `testery list-test-runs --filter Name=project-id,Values=<projectId> --limit 50 --output json` and pick the matching `id` (there is no run-id filter), or from `GET https://api.testery.io/api/test-runs/<runId>` with the API token.

## Status legend

- ✅ passed
- ❌ failed
- ⏭️ skipped / pending / ignored
- 🟡 running / in-progress
- ⚠️ errored / unknown

## Rendering: inline widget, panel, or text

Before rendering the totals summary or per-test breakdown, work out once per session which of three paths is available, in this order: the inline widget, then the same widget shown as a page in a panel, then text.

- Look for a `show_widget` tool from a `visualize` MCP server (it may appear as `visualize:show_widget`, `mcp__visualize__show_widget`, or similar). If your harness supports deferred-tool discovery, do one search for it (e.g. `select:mcp__visualize__show_widget`) — don't repeat the search on later calls in the same session.
- **If found:** build a small, self-contained HTML snippet — totals, a status pill (✅/❌/⚠️), and one row per test with the same ✅/❌/⏭️/🟡/⚠️ semantics as below — and pass it to `show_widget` to render inline. No external scripts/styles/fonts *except* the Testery logo image below; the widget sandboxes content. If the call errors, don't retry it for the rest of the session — use the panel path below for the remainder.

  Include, above the totals:
  - **Logo:** the Testery wordmark, served from jsDelivr — one of the handful of hosts the widget sandbox's CSP allows. Do not link it from `testery.com`; that host is blocked and the image silently renders empty.

    ```html
    <img src="https://cdn.jsdelivr.net/gh/testery/claude-plugin@cebf62ca1872ff0b6bcc88caf640ae5060b2b216/assets/testery-black-wide-logo.png" alt="Testery" style="height:28px">
    ```

    The ref is pinned to a commit deliberately: jsDelivr caches a branch ref like `@main` for about 12 hours, while a commit or tag ref is immutable and served straight away. If the wordmark is ever replaced, update `assets/testery-black-wide-logo.png` and repoint this URL at the new commit.

    It's a dark/black wordmark, so wrap it in a container with an explicit light/white background (e.g. `background:#fff; padding:8px 12px; border-radius:6px;`) so it stays legible regardless of the surrounding theme — don't rely on the page background.
  - **Pass/fail pie chart:** a CSS `conic-gradient` circle (no chart library needed) sized ~120px, one segment per status present (passed/failed/ignored+notRun+timeout grouped as "skipped"), plus a small legend with counts and percentages. Compute each segment's degrees from its share of `totalCount` (360° × share), stacking cumulatively. Colors: passed `#22c55e`, failed `#ef4444`, skipped `#9ca3af`. Example for 33 passed / 1 failed / 0 skipped out of 34 (97.06% / 2.94%):
    ```html
    <div style="width:120px;height:120px;border-radius:50%;
         background:conic-gradient(#22c55e 0deg 349.4deg, #ef4444 349.4deg 360deg);"></div>
    ```
    If every test is the same status (0% or 100% split), render a solid circle in that status's color rather than a degenerate gradient.
  - **Status filter pills:** directly above the per-test list, a row of pills — `All <total>`, `Passed <n>`, `Failed <n>`, plus `Skipped <n>` only when that count is non-zero — that filter the list client-side. Wire them up in the trailing `<script>` (it runs after streaming completes): toggle each test row's `display`, hide any feature-file group left with no visible rows, update a live `Showing <x> of <total>` count in an `aria-live="polite"` element, and set `aria-pressed` on each pill. Do the filtering in JS — never round-trip through `sendPrompt` for it. Order the pills `Failed`, `Passed`, `All`, and open on `Failed` whenever the run has at least one failure — that is what the reader came for, and it saves scrolling past a long list of passes. Fall back to `All` when nothing failed, so a green run never opens on an empty list. Apply the default in the trailing script, after every row has streamed, and show a "No tests match this filter." line if a pill ever yields an empty list. Style the active pill with `background:var(--bg-accent); color:var(--text-accent); border-color:var(--border-accent)` and leave the inactive ones transparent with `var(--border-strong)`.
  - **Links back to Testery:** make the widget clickable. The run title and a `View results` action link to the run page; every test row links to its own result (`.../tests/<testId>`); a failed test additionally gets `Console & video` (`.../tests/<testId>/console`); and an action row carries `Rerun tests` (the run page — see below) and `All runs` (`/test-runs`). Plain `<a href="https://...">` is enough — the host intercepts the click and shows its own link-confirmation dialog. Only emit a per-test link when you hold a real `<testId>` from the results API; never synthesize or extrapolate one.
  - **Fix action on failed tests:** give every failed row — and the failure callout — a wrench button (Tabler `ti-tool`, paired with a visible `Fix` label so the control stays identifiable if the glyph doesn't load) that copies the autofix command to the clipboard. The command is `/testery:autofix-failed-test-run <runId>`. Note it is scoped to a *run*, not a test: it accepts a run id or run URL only, so every failed row copies the same string. Copy with `navigator.clipboard.writeText`, fall back to an offscreen `<textarea>` plus `document.execCommand("copy")` when the sandbox refuses clipboard access, and if both fail render the command in a focused read-only `<input>` for manual copying — a click must never end with nothing visible happening. Confirm the copy in a popup anchored to the button that was clicked ("Copied … — paste it into Claude Code to start the fix"), not in a banner elsewhere in the widget: the list is long, the host page scrolls the iframe, and a confirmation at the top is simply off-screen when the click happened near the bottom. Give the widget's outermost element `position: relative`, append one reusable `position: absolute` popup (`role="status"`) to it, and on each click position it from the button's `getBoundingClientRect()` minus the wrapper's — below the button by default, flipped above when it would extend past the wrapper's height, and clamped horizontally so it stays inside. Dismiss it after about five seconds, on the next click elsewhere, and whenever a filter pill changes the list. Never use `position: fixed`: fixed elements collapse the iframe's height to nothing.
- **If not found** (e.g. running in Claude Code CLI / VS Code / a Claude Code session viewed from the app, where `visualize` isn't exposed), or the widget call fails: show the **same widget as a page in a panel**. Build the fragment exactly as above, then:
  1. **Inline the logo.** Panels and Artifact pages only load images from the page itself, so replace the jsDelivr `src` with a data URI of `${CLAUDE_PLUGIN_ROOT}/assets/testery-black-wide-logo.png` (`data:image/png;base64,` + `base64 -w0` of the file; on PowerShell, `[Convert]::ToBase64String([IO.File]::ReadAllBytes(...))`). Keep the white container around it.
  2. **Wrap it in the shell.** Read `${CLAUDE_PLUGIN_ROOT}/skills/testery-report-test-run/panel-shell.html`, replace `<!-- WIDGET -->` with the fragment and `__RUN_ID__` with the run id, and write the result to `testery-run-<runId>.html` in the session's scratchpad or temp directory. The shell defines the host tokens the fragment relies on (`--text-primary`, `--surface-1`, `--bg-danger`, `--border-strong`, …) for light and dark, gives the page a `<title>` and background, and makes Testery links open in a new tab, since no host intercepts the click. Don't restyle the fragment; if it needs a token the shell lacks, add the token to the shell. The Tabler icon font doesn't load there, which is why the `Fix` buttons carry a visible label.
  3. **Show it**, trying each of these once per session and moving on if it's missing or refused:
     - `SendUserFile` with `display: "render"` and a one-line caption (verdict + totals), which opens the page in the side panel. If it reports the file was not delivered (e.g. "not on a project thread"), move on.
     - The `Artifact` tool: publish the file (`icon: "check"` on the first publish, a one-sentence `description` naming the run and project). Re-publishing the same file path updates the same page, so reuse `testery-run-<runId>.html` when reporting the same run again. Give the user the link and note the page is private until they share it.
     - Neither available: use the text formatting below.

  Whichever panel path succeeds, still print the text totals summary from step 2 in the chat, so the verdict is in the transcript without opening the panel. Skip the per-test text list when the panel shows it.
- **Text** is the always-available last resort: use the formatting below. Don't ask the user to choose a path, and don't block waiting on these checks.

## Steps

1. Fetch the totals line and the per-test JUnit XML:
   ```bash
   TESTERY_SKILL="testery-report-test-run" testery report-test-run --test-run-id <id>
   TESTERY_SKILL="testery-report-test-run" testery report-test-run \
     --test-run-id <id> \
     --output junit \
     --outfile <scratch-dir>/testery-run-<id>.xml
   ```
   Then get the run details (status, start/end time, branch, commit) as described under "Run details" above. Duration is `endTime − startTime`.

2. Render a totals summary (inline widget, panel, or text — see "Rendering" above). Include the run URL on the header line (see "Testery URLs" below):

   ```
   Testery Test Run <id>  ·  <project> @ <env>
   https://testery.app/<accountName>/test-runs/<runId>
   ─────────────────────────────────────────────
   Total: 34   ✅ 33   ❌ 1   ⏭️ 0     Duration: 7m43s
   Status: ❌ FAILED
   ```

   Map `status` to a verdict emoji: `PASS`/`PASSED` → ✅, `FAIL`/`FAILED` → ❌, `RUNNING`/`IN_PROGRESS`/`QUEUED` → 🟡, anything else → ⚠️ (include the raw status).

3. **For a per-test breakdown** (when the user wants individual scenarios), read the tests from the JUnit XML (or the Testery MCP `get_test_results`, when connected) and render one line per test (inline widget, panel, or text). Link each failing test to its console page:

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

**Getting `<testId>`:** `report-test-run` never emits test IDs; neither the JUnit nor the SonarQube output carries them. Fetch them from `GET https://api.testery.io/api/test-runs/<runId>/results`, which returns one object per test carrying `id` (the `<testId>`), `status`, `duration`, and `projectTest.name`.

**Rerun is an action, not a URL.** The app reruns via `POST /api/test-runs/<runId>/rerun`; no GET route triggers one, and the widget sandbox is unauthenticated. A `Rerun tests` control must therefore link to the run page, where the app's own rerun buttons live. Do not link to `/test-runs/<runId>/rerun` — there is no such tab, and it silently lands on the results page.

## CI use

For a non-interactive check, pass `--fail-on-failure` so the CLI itself exits non-zero on failures:

```bash
TESTERY_SKILL="testery-report-test-run" testery report-test-run --test-run-id <id> --fail-on-failure
```

In CI, set `$TESTERY_API_TOKEN` (or pass `--token`). Add `--output junit --outfile testery-results.xml` to publish the per-test results as a test report, e.g. with Azure DevOps `PublishTestResults@2`, Jenkins or GitLab.
