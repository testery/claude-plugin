---
name: testery-update-environment
description: Update an existing Testery environment (rename, change pipeline stage, set/replace variables). Use when modifying an env that already exists.
---

# Update a Testery environment

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`) (`${CLAUDE_PLUGIN_ROOT}` is the plugin root: set by Claude Code; in GitHub Copilot or another agent, use the plugin folder that holds this skill's `skills/` directory). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then ask the user (with the **AskUserQuestion** tool if your agent has it) to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery update-environment`.

```bash
TESTERY_SKILL="testery-update-environment" testery update-environment \
  --token "$TESTERY_TOKEN" \
  --key "<env-key>" \
  [--name "<New Name>"] \
  [--pipeline-stage "<stage>"] \
  [--variable KEY=VALUE] \
  [--create-if-not-exists]
```

Pass `--create-if-not-exists` to upsert (create when the key isn't found).
