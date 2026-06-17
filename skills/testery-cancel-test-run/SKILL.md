---
name: testery-cancel-test-run
description: Cancel a running Testery test run by ID. Use when the user asks to "stop", "abort", or "cancel" a Testery run.
---

# Cancel a Testery test run

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery cancel-test-run`.

```bash
testery cancel-test-run \
  --token "$TESTERY_TOKEN" \
  --test-run-id <id>
```

## Steps

1. Confirm the test run ID with the user (cancellation is destructive).
2. Run the command and report the result.
