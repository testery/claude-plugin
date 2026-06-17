---
name: testery-list-test-runs
description: List recent Testery test runs, optionally filtered by branch, status, environment, project, name, or phase. Use when the user asks "show recent runs", "what runs failed?", "list test runs for branch X", or "/testery-list-test-runs".
---

# List Testery test runs

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery list-test-runs`. Lists recent test runs (most recent first), optionally filtered.

```bash
testery list-test-runs \
  --token "$TESTERY_TOKEN" \
  [--limit <1-50>] \
  [--filter Name=<field>,Values=<v1>,<v2>] \
  [--output pretty|json]
```

Flags:
- `--limit <N>`: maximum number of runs to return (1–50, default 10).
- `--filter Name=<field>,Values=<v1>,<v2>`: AWS-CLI–style filter. Supported `<field>` values: `branch`, `environment-id`, `name`, `phase`, `project-id`, `status`. Repeat `--filter` for multiple filters (AND-ed together).
- `--output pretty|json`: output format (default `pretty`).
- Auth: `--token` / `--profile`, falling back to `~/.testery/credentials` or `$TESTERY_API_TOKEN`.

## Examples

Last 5 failed runs:
```bash
testery list-test-runs --token "$TESTERY_TOKEN" --limit 5 \
  --filter Name=status,Values=FAIL
```

Runs on a branch that passed or failed:
```bash
testery list-test-runs --token "$TESTERY_TOKEN" \
  --filter Name=branch,Values=main \
  --filter Name=status,Values=PASS,FAIL
```

## Testery URLs

When listing runs to the user, include each run's URL. Testery app URLs follow `https://testery.app/<accountName>/<page>`, where `<accountName>` is the account slug in your Testery URLs (e.g. `testery-qa`):

- Test run: `https://testery.app/<accountName>/test-runs/<runId>`

Resolve `<accountName>` from `$TESTERY_ACCOUNT_SLUG`, or the run JSON's `account.name`/`account.slug` if present. Prefer `--output json` when constructing URLs so you can read each run's account/id reliably.
