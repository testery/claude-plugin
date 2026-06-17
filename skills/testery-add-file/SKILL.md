---
name: testery-add-file
description: Attach a file (artifact, log, or input) to an existing Testery test run. Use to add context to a run after it has been created.
---

# Add a file to a test run

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery add-file`. The file path is a **positional argument** (`FILE_PATH`), not a flag.

```bash
testery add-file ./path/to/file \
  --token "$TESTERY_TOKEN" \
  --test-run-id <id> \
  [--kind <KIND>]
```

Flags:
- `FILE_PATH` (positional, required): the local file to attach.
- `--test-run-id <id>`: the test run to attach the file to.
- `--kind <KIND>`: the kind of file being uploaded (e.g. pass `DotCover` for a DotCover JSON coverage file).
- Auth: `--token` / `--profile`, falling back to `~/.testery/credentials` or `$TESTERY_API_TOKEN`.
