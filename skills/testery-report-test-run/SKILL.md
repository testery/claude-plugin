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

2. Render a totals summary. Include the run URL on the header line (see "Testery URLs" below):

   ```
   Testery Test Run <id>  ·  <project> @ <env>
   https://testery.app/<accountName>/test-runs/<runId>
   ─────────────────────────────────────────────
   Total: 34   ✅ 33   ❌ 1   ⏭️ 0     Duration: 7m43s
   Status: ❌ FAILED
   ```

   Map `status` to a verdict emoji: `PASS`/`PASSED` → ✅, `FAIL`/`FAILED` → ❌, `RUNNING`/`IN_PROGRESS`/`QUEUED` → 🟡, anything else → ⚠️ (include the raw status).

3. **For a per-test breakdown** (when the user wants individual scenarios), pull results from the Testery MCP `get_test_results` and render one line per test. Link each failing test to its console page:

   ```
   ✅ login.feature › User logs in successfully           1.2s
   ❌ checkout.feature › User completes checkout          3.4s
       → AssertionError: expected "Order placed" got "Error"
       → https://testery.app/<accountName>/test-runs/<runId>/tests/<testId>/console
   ⏭️ profile.feature › Avatar upload (skipped: @wip)
   ```

   For failed tests, include the error/stack snippet beneath the line (indented `    →`; truncate long stacks to ~5 lines) and a link to its console page.

## Testery URLs

Testery app URLs follow `https://testery.app/<accountName>/<page>`, where `<accountName>` is the account slug shown in your Testery URLs (e.g. `testery-qa`):

- Test run: `https://testery.app/<accountName>/test-runs/<runId>`
- A single test's console (logs/screenshots/video; use for failures): `https://testery.app/<accountName>/test-runs/<runId>/tests/<testId>/console`

Resolve `<accountName>` from `$TESTERY_ACCOUNT_SLUG`, or from the run JSON's `account.name`/`account.slug` if present. If neither is available, print the URL with the `<accountName>` placeholder and ask the user to set `TESTERY_ACCOUNT_SLUG`.

## CI use

For a non-interactive check, pass `--fail-on-failure` so the CLI itself exits non-zero on failures:

```bash
TESTERY_SKILL="testery-report-test-run" testery report-test-run --token "$TESTERY_TOKEN" --test-run-id <id> --fail-on-failure
```
