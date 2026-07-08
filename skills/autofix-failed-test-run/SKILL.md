---
name: autofix-failed-test-run
description: Diagnose a failed Testery test run and fix it — pulls the run's failures, finds the root cause, then per root cause asks whether to update the test, fix the app bug, or file a bug report. Use when the user says "autofix", "fix my failing tests", "why did my test run fail", "/testery:autofix-failed-test-run", or hands you a Testery run id / URL to repair.
---

# Autofix a failed Testery test run

The flagship "wow" command: point it at a failed Testery run (or let it grab the latest),
and it walks each root cause with you — **update the test**, **fix the bug**, or **file a bug
report**. It never changes anything without asking.

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

## 1. Require an authenticated account (hard requirement)

This command **requires a logged-in Testery account** — it reads a specific account's runs and
their failure artifacts. Confirm auth *and* surface which account you're acting on before doing
anything else:

```bash
TESTERY_SKILL="autofix-failed-test-run" testery verify-token
```

- Prints `Valid token` → authenticated; continue.
- Anything else (`Invalid token`, an error, or the CLI reports `NOT_ONBOARDED`) → **run the
  `testery-onboard` skill** to log in, then re-check. Do not proceed unauthenticated.

The fetch helper in step 3 also returns the resolved **account** (id + slug). Tell the user which
account you're operating on, e.g. `Authenticated as **upbeatjones**`, so they can confirm it's the
right one. If it's the wrong account, they can switch with `testery login --profile <name>` (pass
`--profile` through to the helper).

## 2. Resolve the target run

- **Argument given** — the user passed a run id (`1010984`) or a run URL
  (`https://testery.app/<account>/test-runs/1010984`). Use it as-is; the helper parses either form.
- **No argument** — use the account's **latest** run (`--latest`).

## 3. Fetch the failures (bundled helper)

Run the bundled `fetch_failures.py`. It resolves the token/account the same way the CLI does
(`--token` / `$TESTERY_API_TOKEN` / `~/.testery/credentials`), finds the run, and returns a compact
JSON bundle — the account, the run summary, and per **FAILED** test: name, file, the error, a tail
of the runner output, and screenshot/video URLs.

- POSIX shell (macOS, Linux, Git Bash):
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/autofix-failed-test-run/bin/fetch_failures.py" <RUN_ID_OR_URL>
  # or, for the most recent run:
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/autofix-failed-test-run/bin/fetch_failures.py" --latest
  ```
- Windows PowerShell:
  ```powershell
  python "${CLAUDE_PLUGIN_ROOT}/skills/autofix-failed-test-run/bin/fetch_failures.py" <RUN_ID_OR_URL>
  ```

(Use `python`, `python3`, or the `py -3` launcher depending on the OS.) Pass `--profile <name>` to
target a non-default credentials profile.

Handle the bundle:
- `error: unauthenticated` / `error: no_token` → run the **testery-onboard** skill, then retry.
- `error: no_runs` / `error: run_not_found` → tell the user; offer to list runs
  (`testery-list-test-runs`).
- `run.status` is `RUNNING`/`QUEUED` → the run isn't finished; offer to monitor it first
  (`testery-monitor-test-run`) and stop.
- `failureCount == 0` → nothing to fix; report the run passed and stop.

Everything the results endpoint knows about a failure is in the bundle. If you need more, the
screenshot/video URLs are presigned — you may fetch a screenshot to confirm a UI-level failure.

## 4. Diagnose and group by root cause

Read each failure's `error` + `outputTail`. **Group failures that share one root cause** (e.g. five
tests all failing on the same changed selector = one root cause). Common shapes:

- **Stale test / broken locator / changed copy or route** — the app changed and the test wasn't
  updated (e.g. `strict mode violation: locator(...) resolved to 2 elements`, `Timed out waiting
  for selector`, an assertion on old expected text). → usually **update the test**.
- **Real application bug** — the app is genuinely wrong (a 500, a broken flow, wrong computed
  value). → usually **fix the bug**.
- **Environment/flake/infra** — timeout with no code cause, auth/network blip, data not seeded.
  → often **file a bug report** (or re-run), don't change code blindly.

Present a short, human diagnosis per root cause: what failed, the tests it accounts for, the
evidence (trimmed error / a screenshot link), and your best guess at the category.

## 5. Per root cause, ask what to do (required)

For **each distinct root cause**, use the **AskUserQuestion** tool to let the user choose. Ask one
question per root cause (batch them if there are several), header e.g. `Root cause 1`, with these
three options:

1. **Update the test** — the test is out of date; change the test/page-object/step to match the
   app's new behavior. (Recommended when the app is behaving correctly.)
2. **Fix the bug** — it's a real application bug; change the app code so the test passes.
3. **File a bug report** — don't fix now; write up the root cause for later.

Include your recommendation as the first option's framing. Then act on the choice:

- **Update the test** → locate the test in the working copy (use the failure's `fileFilter` /
  `file` and the scenario `name`). Fix the test/page-object/step definition — **not** by weakening
  assertions, but to match the app's real, correct behavior. Prefer stable locators (add or use a
  `data-testid`). Re-run just that test with the `testery-playwright-bdd-run-local` skill
  (`--grep "<scenario>"`) until green. For adding/repairing scenarios or step defs, hand off to
  `testery-playwright-bdd-add-scenario` / `testery-playwright-bdd-add-step-definition`.
- **Fix the bug** → hand off to the `testery-playwright-bdd-implement-code` skill to change
  **application code** (not the `.feature` text) until the scenario passes locally.
- **File a bug report** → write the report (next section).

If there is no local checkout of the tests/app (the user only has a Testery run), you can still
diagnose and file a bug report; explain that updating the test or fixing the bug needs the repo
open.

## 6. Filing a bug report

Write a Markdown report to `./testery-bug-reports/run-<runId>-cause-<n>.md` (create the dir).
Include:

- **Title** — one line naming the root cause.
- **Testery run** — the run URL and status/counts.
- **Category** — stale test / app bug / environment-flake.
- **Affected tests** — each scenario name + file.
- **Evidence** — the trimmed error and a screenshot/video link (the presigned URLs from the
  bundle).
- **Suggested fix** — your recommended remediation.

Then tell the user where it was written. If a GitHub CLI (`gh`) or an issue-tracker MCP is
available and the user wants it filed there, offer to open an issue from the same content — but the
local file is the default so this works with no extra setup.

## 7. Wrap up

Summarize what changed and what's left: per root cause, the choice made and the outcome (test green
locally / app fix applied / report filed). If tests were changed or code was fixed, suggest
re-running the suite on Testery (`testery-playwright-bdd-run-on-testery-remote`) or monitoring a
fresh run (`testery-monitor-test-run`) to confirm the run is green end-to-end.

## Testery URLs

Testery app URLs follow `https://testery.app/<accountName>/<page>`, where `<accountName>` is the
account slug (the `account.name` in the fetch bundle):

- Test run: `https://testery.app/<accountName>/test-runs/<runId>`
- A single test's console (logs/screenshots/video): `https://testery.app/<accountName>/test-runs/<runId>/tests/<testId>/console`

The bundle already builds `run.url` for you from the resolved account slug.
