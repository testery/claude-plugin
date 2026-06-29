---
name: testery-upload-artifacts
description: Upload a local file or directory of build artifacts to Testery, associated with a build ID. Use this to ship a local test bundle (e.g., a playwright-bdd project) up to Testery so it can be executed remotely.
---

# Upload build artifacts

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

Wraps `testery upload-build-artifacts`. Uploads a file or a directory (zipped automatically) and ties it to a `build-id` that you can later reference from `create-test-run --build-id`.

## Template

Single file:
```bash
TESTERY_SKILL="testery-upload-artifacts" testery upload-build-artifacts \
  --token "$TESTERY_TOKEN" \
  --project-key "<project>" \
  --build-id "<unique-id>" \
  --path ./dist/tests.zip \
  [--branch "<branch>"]
```

Directory: pre-zip with explicit excludes, then upload the zip. This keeps bundles small and avoids shipping secrets, virtualenvs, or build caches:

```bash
# Excludes: VCS, deps, virtualenvs, build/test caches, IDE/editor, OS junk, env files.
zip -r /tmp/bundle.zip . \
  -x '.git/*' '.gitignore' \
     'node_modules/*' \
     '.venv/*' 'venv/*' 'env/*' '.env' '.env.*' \
     '__pycache__/*' '*.pyc' '.pytest_cache/*' '.mypy_cache/*' '.ruff_cache/*' '.tox/*' \
     'dist/*' 'build/*' '.next/*' '.nuxt/*' 'target/*' 'out/*' 'coverage/*' '.nyc_output/*' \
     '.idea/*' '.vscode/*' \
     '.DS_Store' 'Thumbs.db'

TESTERY_SKILL="testery-upload-artifacts" testery upload-build-artifacts \
  --token "$TESTERY_TOKEN" \
  --project-key "<project>" \
  --build-id "<unique-id>" \
  --path /tmp/bundle.zip \
  [--branch "<branch>"]
```

On Windows PowerShell, use `Compress-Archive` with a filtered file list (e.g., `Get-ChildItem -Recurse | Where-Object { $_.FullName -notmatch '\\(\.git|node_modules|\.venv|venv|__pycache__|dist|build|coverage)\\' }`) and pipe to `Compress-Archive -DestinationPath bundle.zip`.

## Steps

1. Pick a `build-id` (timestamp, git short SHA, or CI build number: must be unique within the project).
2. Pre-zip the directory with the excludes above (skip this if uploading a single pre-built file).
3. Upload with `--path <zip>`.
4. Hand the same `build-id` to `testery create-test-run --build-id <id>` to execute the uploaded code.

## Common pairing

- `testery-cli-setup` → `testery-upload-artifacts` → `testery-create-test-run` (with `--build-id`) → `testery-monitor-test-run`.
