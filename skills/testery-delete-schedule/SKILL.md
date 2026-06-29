---
name: testery-delete-schedule
description: Delete a Testery schedule by name. Use when the user wants to remove a recurring/triggered schedule.
---

# Delete a Testery schedule

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery delete-schedule`.

```bash
TESTERY_SKILL="testery-delete-schedule" testery delete-schedule \
  --token "$TESTERY_TOKEN" \
  --name "<schedule-name>"
```
