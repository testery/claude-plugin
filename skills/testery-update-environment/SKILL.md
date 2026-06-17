---
name: testery-update-environment
description: Update an existing Testery environment (rename, change pipeline stage, set/replace variables). Use when modifying an env that already exists.
---

# Update a Testery environment

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery update-environment`.

```bash
testery update-environment \
  --token "$TESTERY_TOKEN" \
  --key "<env-key>" \
  [--name "<New Name>"] \
  [--pipeline-stage "<stage>"] \
  [--variable KEY=VALUE] \
  [--create-if-not-exists]
```

Pass `--create-if-not-exists` to upsert (create when the key isn't found).
