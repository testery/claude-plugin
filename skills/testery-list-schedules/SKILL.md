---
name: testery-list-schedules
description: List the Testery schedules (interval/cron and deploy triggers) configured for the account. Use when the user asks "what's scheduled?", "show me the test run schedules", "list schedules", or "/testery-list-schedules".
---

# List Testery schedules

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`) (`${CLAUDE_PLUGIN_ROOT}` is the plugin root: set by Claude Code; in GitHub Copilot or another agent, use the plugin folder that holds this skill's `skills/` directory). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then ask the user (with the **AskUserQuestion** tool if your agent has it) to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery list-schedules`. Lists the schedules (triggers) configured for the account.

```bash
TESTERY_SKILL="testery-list-schedules" testery list-schedules \
  --token "$TESTERY_TOKEN" \
  [--show-archived] \
  [--output pretty|json]
```

Flags:
- `--show-archived`: include archived schedules in the output.
- `--output pretty|json`: output format (default `pretty`).
- Auth: `--token` / `--profile`, falling back to `~/.testery/credentials` or `$TESTERY_API_TOKEN`.

Prefer `--output json` when you need to read each schedule's fields (name, type, cron, project/environment) reliably; render a short per-schedule summary for the user otherwise.
