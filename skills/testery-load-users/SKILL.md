---
name: testery-load-users
description: Bulk-load users into a Testery account from a JSON/CSV file. Use for organization onboarding.
---

# Load Testery users

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`) (`${CLAUDE_PLUGIN_ROOT}` is the plugin root: set by Claude Code; in GitHub Copilot or another agent, use the plugin folder that holds this skill's `skills/` directory). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then ask the user (with the **AskUserQuestion** tool if your agent has it) to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery load-users`.

```bash
TESTERY_SKILL="testery-load-users" testery load-users \
  --token "$TESTERY_TOKEN" \
  --user-file ./users.json
```

Confirm the file format with the user before running: this is a write operation that affects org membership.
