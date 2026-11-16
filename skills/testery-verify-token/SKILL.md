---
name: testery-verify-token
description: Verify a Testery API token is valid and report the associated user. Use as a quick auth health check.
---

# Verify a Testery API token

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`) (`${CLAUDE_PLUGIN_ROOT}` is the plugin root: set by Claude Code; in GitHub Copilot or another agent, use the plugin folder that holds this skill's `skills/` directory). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then ask the user (with the **AskUserQuestion** tool if your agent has it) to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery verify-token`.

```bash
TESTERY_SKILL="testery-verify-token" testery verify-token --token "$TESTERY_TOKEN"
```
