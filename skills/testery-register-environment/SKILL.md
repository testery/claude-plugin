---
name: testery-register-environment
description: Register (create) a new Testery environment that tests can target. Use when the user wants to add a new env (e.g., "staging", "qa", "prod") to Testery.
---

# Register a Testery environment

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery create-environment`.

```bash
testery create-environment \
  --token "$TESTERY_TOKEN" \
  --key "<env-key>" \
  --name "<Display Name>" \
  [--pipeline-stage "<stage-name>"] \
  [--variable KEY=VALUE]   # repeat; prefix `secure:` to encrypt
```

## Steps

1. Get the desired key (used in test runs) and display name.
2. Optionally collect environment variables and a pipeline stage.
3. Run the command and report the resulting environment.

To update an existing environment instead, use `testery-update-environment`.
