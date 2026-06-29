---
name: testery-upload-environment-file
description: Upload a file (e.g., a config, fixture, or credential file) and attach it to a Testery environment. Use to make the file available to tests running in that env.
---

# Upload a file to a Testery environment

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery upload-environment-file`.

```bash
TESTERY_SKILL="testery-upload-environment-file" testery upload-environment-file \
  --token "$TESTERY_TOKEN" \
  --environment-key "<env-key>" \
  --file-name "<remote-name>" \
  --source-path ./path/to/local/file
```
