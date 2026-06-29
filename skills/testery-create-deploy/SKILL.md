---
name: testery-create-deploy
description: Notify Testery that a deploy occurred for a project + environment. Triggers any deploy-type schedules attached to that environment. Use from CI after a deploy lands.
---

# Create a Testery deploy event

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery create-deploy`.

```bash
TESTERY_SKILL="testery-create-deploy" testery create-deploy \
  --token "$TESTERY_TOKEN" \
  --project "<project-key>" \
  --environment "<env-key>" \
  [--commit <sha>] [--branch <name>] [--build-id <id>] \
  [--git-provider GitHub --git-owner <org> --git-repo <repo>] \
  [--wait-for-results --fail-on-failure --output pretty|json|teamcity]
```

`--wait-for-results` blocks until all triggered test runs finish.
