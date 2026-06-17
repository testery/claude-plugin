---
name: testery-list-active-test-runs
description: List currently-active Testery test runs and their status. Use when the user asks "what's running?" or wants an overview of in-flight runs.
---

# List active test runs

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery list-active-test-runs`.

```bash
testery list-active-test-runs \
  --token "$TESTERY_TOKEN" \
  [--output pretty|json]
```

When listing runs to the user, include the run URL for each one. Testery app URLs follow `https://testery.app/<accountName>/<page>` (where `<accountName>` is the account slug in your Testery URLs, e.g. `testery-qa`):

```
https://testery.app/<accountName>/test-runs/<runId>
```

Resolve `<accountName>` from `$TESTERY_ACCOUNT_SLUG`, or the run JSON's `account.name`/`account.slug` if present. Prefer JSON output (`--output json`) when constructing URLs so you can read each run's account/id reliably.

For richer read-only inspection (per-project listing, completed runs, results) the Testery MCP server's `list_test_runs` and `get_test_results` tools are a good alternative when configured.
