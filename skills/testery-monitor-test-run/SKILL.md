---
name: testery-monitor-test-run
description: Follow a Testery test run with a live ANSI dashboard (progress bar, counts, ETA, currently-running tests) and report a final pass/fail summary with emojis. Use after creating a test run, or when the user asks to "watch", "monitor", "wait for", or "tail" a Testery run.
---

# Monitor a Testery test run (live ANSI dashboard)

While a run is in flight, render a live multi-line dashboard:

```
╭─────────────────────────────────────────────────────────────╮
│ Testery · run 12345 · proj-foo @ staging                    │
│                                                             │
│ ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  30%      │
│                                                             │
│ ✅ 11 passed   ❌  1 failed   ⏭  0 skipped   🟡  3 running │
│ ⏱  elapsed: 02:14   eta: ~05:30   queued: 25 / total: 40   │
│                                                             │
│ Now running:                                                │
│   🟡 login.feature › User logs in successfully              │
│   🟡 checkout.feature › Cart shows items                    │
│   🟡 profile.feature › Avatar upload                        │
╰─────────────────────────────────────────────────────────────╯
```

The dashboard is implemented as a helper that ships with this skill collection: it polls the Testery API every few seconds, redraws in place using ANSI escapes (`ESC[<n>A` to move up, `ESC[2K` to clear lines), and hides/restores the cursor via `ESC[?25l` / `ESC[?25h`. Resize-tolerant: width is re-read each frame.

## Steps

1. Resolve the test run ID (from a prior `create-test-run`, the user, or `testery list-active-test-runs`).

2. Launch the live dashboard:

   **bash / git bash / macOS / Linux:**
   ```bash
   ~/.claude/skills/testery-monitor-test-run/bin/testery-watch.sh <run-id>
   #   options: --poll 3   --token "$TESTERY_TOKEN"   --api https://api.testery.io
   ```

   **PowerShell:**
   ```powershell
   & "$HOME\.claude\skills\testery-monitor-test-run\bin\testery-watch.ps1" <run-id>
   ```

   The script auto-loads the token from `$TESTERY_TOKEN` or `~/.testery/credentials`. It exits 0 on success, 1 on failure: propagate that for CI.

3. After the dashboard exits, render the final per-test summary using the format from `testery-report-test-run`. Include the run URL on the header line (see "Testery URLs" below):

   ```
   Testery Test Run <id>  ·  <project> @ <env>
   https://testery.app/<accountName>/test-runs/<runId>
   ─────────────────────────────────────────────
   ✅ login.feature › User logs in successfully           1.2s
   ❌ checkout.feature › User completes checkout          3.4s
       → AssertionError: expected "Order placed" got "Error"
       → https://testery.app/<accountName>/test-runs/<runId>/tests/<testId>/console
   ⏭️ profile.feature › Avatar upload (skipped: @wip)
   ─────────────────────────────────────────────
   Total: N   ✅ p   ❌ f   ⏭️ s     Duration: T
   Status: ✅ PASSED   (or ❌ FAILED)
   ```

   For each failed test, include a direct link to its console page (`/test-runs/<runId>/tests/<testId>/console`) beneath the error so the user can jump straight to logs/screenshots/video.

   Status mapping:
   - `PASS`/`PASSED` → ✅
   - `FAIL`/`FAILED` → ❌
   - `SKIP`/`SKIPPED`/`PENDING`/`IGNORED` → ⏭️
   - `RUNNING`/`IN_PROGRESS`/`QUEUED` → 🟡
   - anything else → ⚠️ (include raw status)

## When the dashboard isn't appropriate

Use the plain CLI form (no animation) for non-TTY contexts (CI logs, piped output, NO_COLOR set):

```bash
testery monitor-test-run --token "$TESTERY_TOKEN" --test-run-id <id> --output json [--fail-on-failure]
```

The watch script auto-detects non-TTY and disables color, but for CI you usually want simple line-oriented output instead: prefer `monitor-test-run` directly with `--fail-on-failure`.

## All active runs in a time window

```bash
testery monitor-test-runs --token "$TESTERY_TOKEN" --duration <minutes>
```

Render each completed run as a one-liner. Each line should also include the run URL (`https://testery.app/<accountName>/test-runs/<id>`) on the right or beneath:

```
✅ run 12345  ·  proj-foo @ staging   12/12 passed   2m4s   https://testery.app/<accountName>/test-runs/12345
❌ run 12346  ·  proj-bar @ qa        9/10 passed    3m11s  https://testery.app/<accountName>/test-runs/12346
🟡 run 12347  ·  proj-baz @ dev       in progress           https://testery.app/<accountName>/test-runs/12347
```

## Testery URLs

Testery app URLs follow `https://testery.app/<accountName>/<page>`, where `<accountName>` is the account slug shown in your Testery URLs (e.g. `testery-qa`):

- Test run: `https://testery.app/<accountName>/test-runs/<runId>`
- A single test's console (logs/screenshots/video; use for failures): `https://testery.app/<accountName>/test-runs/<runId>/tests/<testId>/console`

Resolve `<accountName>` from `$TESTERY_ACCOUNT_SLUG`, or from the run JSON's `account.name`/`account.slug` if present. If neither is available, print the URL with the `<accountName>` placeholder and ask the user to set `TESTERY_ACCOUNT_SLUG`.

## Dependencies

- `bash` skill: `curl`, `jq`. (`jq` is the only non-default dep: `apt install jq` / `brew install jq` / `choco install jq`.)
- `pwsh` skill: PowerShell 5+ (uses `Invoke-RestMethod`).
