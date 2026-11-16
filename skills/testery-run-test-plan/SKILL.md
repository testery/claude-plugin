---
name: testery-run-test-plan
description: Execute a saved Testery test plan against an environment. Use when the user references running a "test plan" (a curated set of suites/projects).
---

# Run a Testery test plan

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`) (`${CLAUDE_PLUGIN_ROOT}` is the plugin root: set by Claude Code; in GitHub Copilot or another agent, use the plugin folder that holds this skill's `skills/` directory). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then ask the user (with the **AskUserQuestion** tool if your agent has it) to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery run-test-plan`.

```bash
TESTERY_SKILL="testery-run-test-plan" testery run-test-plan \
  --token "$TESTERY_TOKEN" \
  --test-plan-key "<plan-key>" \
  --environment-key "<env-key>" \
  [--variable KEY=VALUE]
```
