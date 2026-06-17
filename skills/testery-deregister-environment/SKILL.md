---
name: testery-deregister-environment
description: Delete (deregister) a Testery environment by key. Use when the user wants to remove an environment from Testery.
---

# Deregister a Testery environment

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery delete-environment`.

```bash
testery delete-environment \
  --token "$TESTERY_TOKEN" \
  --key "<env-key>"
```

## Steps

1. Confirm with the user: deletion is destructive.
2. Run the command.
