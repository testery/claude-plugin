---
name: testery-create-test-run
description: Submit a Git-based test run to Testery. Use when the user asks to "run tests on Testery", "kick off a Testery run", "trigger a test run for branch X", etc.
---

# Create a Testery test run

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery create-test-run`. Submits a test run for a given project + environment, optionally pinned to a Git ref/branch or a previously-uploaded build.

## Required inputs

- `--project-key`: project key in Testery.
- `--environment-key`: environment key the tests run against.
- One of: `--git-ref <sha>`, `--git-branch <name>`, `--build-id <id>` (with prior `upload-build-artifacts`), or `--latest-deploy`.

## Common optional flags

- `--include-tags a,b,c` / `--exclude-tags x,y`: filter scenarios by tag.
- `--test-filter-regex <pattern>`: regex test filter.
- `--parallelize-by-file` or `--parallelize-by-test`.
- `--runner-count <N>`: parallel runners.
- `--copies <N>`: submit multiple copies.
- `--variable KEY=VALUE`: env variable for this run (repeatable; prefix `secure:` to encrypt).
- `--timeout-minutes <N>` / `--test-timeout-seconds <N>`.
- `--wait-for-results`: block until completion (combine with `--fail-on-failure` for CI).
- `--output pretty|json|teamcity`.
- `--test-suite "Name"`: run a saved test suite.

## Template

```bash
testery create-test-run \
  --token "$TESTERY_TOKEN" \
  --project-key "<project>" \
  --environment-key "<env>" \
  --git-branch "<branch>" \
  [--include-tags ...] [--runner-count N] [--wait-for-results --fail-on-failure]
```

## Steps

1. If you don't know the project/environment keys, ask the user, or use the Testery MCP `list_projects` / list environments via `testery list-environments`.
2. Build the command above with the user's inputs.
3. Run it and report `test_run_id` from the output, plus the run URL:
   ```
   https://testery.app/<accountName>/test-runs/<test_run_id>
   ```
   See "Testery URLs" below for resolving `<accountName>`.
4. If the user wants to follow it, use the `testery-monitor-test-run` skill.

## Testery URLs

Testery app URLs follow `https://testery.app/<accountName>/<page>`, where `<accountName>` is the account slug shown in your Testery URLs (e.g. `testery-qa`). Useful pages:

- Test run: `https://testery.app/<accountName>/test-runs/<runId>`
- A single test's console (e.g. to link a failing test): `https://testery.app/<accountName>/test-runs/<runId>/tests/<testId>/console`

Resolve `<accountName>` from `$TESTERY_ACCOUNT_SLUG`, or from an `account.name`/`account.slug` field if present in the JSON response. If neither is available, print the URL with the `<accountName>` placeholder and ask the user to set `TESTERY_ACCOUNT_SLUG`. (There is no `testery whoami` command.)
