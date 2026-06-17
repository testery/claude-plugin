---
name: testery-playwright-bdd-run-on-testery-local-build
description: Run the LOCAL working-copy version of a playwright-bdd project on Testery (zip up the cwd, upload, then create a test run pinned to that build). Use when the user wants to test their uncommitted local changes on Testery infrastructure.
---

# Run local build on Testery

> **Prereq — `testery` CLI:** before the first `testery` call this session, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.sh"` (PowerShell: `& "${CLAUDE_PLUGIN_ROOT}/scripts/detect_testery.ps1"`). `NOT_INSTALLED` → display exactly `Your AI-enabled testing journey with Testery is about to begin! 🤖` then use the **AskUserQuestion** tool to offer installing the Testery CLI (install per `testery-cli-setup` if yes). `NOT_ONBOARDED` → run the **testery-onboard** skill to authenticate. `READY` → proceed. Don't re-check before every command.

This wraps the CLI flow:
1. Pre-zip the project dir with excludes (see below), then `testery upload-build-artifacts` ships the zip.
2. `testery create-test-run --build-id ...`: runs against that uploaded bundle.

## Template

```bash
BUILD_ID="local-$(date +%s)"

# Exclude VCS, deps, virtualenvs, build/test caches, IDE/editor, OS junk, env files,
# plus playwright/playwright-bdd outputs that don't belong in the bundle.
zip -r /tmp/bundle.zip . \
  -x '.git/*' '.gitignore' \
     'node_modules/*' \
     '.venv/*' 'venv/*' 'env/*' '.env' '.env.*' \
     '__pycache__/*' '*.pyc' '.pytest_cache/*' '.mypy_cache/*' '.ruff_cache/*' '.tox/*' \
     'dist/*' 'build/*' '.next/*' '.nuxt/*' 'target/*' 'out/*' 'coverage/*' '.nyc_output/*' \
     'playwright-report/*' 'test-results/*' '.features-gen/*' \
     '.idea/*' '.vscode/*' \
     '.DS_Store' 'Thumbs.db'

testery upload-build-artifacts \
  --token "$TESTERY_TOKEN" \
  --project-key "<project>" \
  --build-id "$BUILD_ID" \
  --path /tmp/bundle.zip

testery create-test-run \
  --token "$TESTERY_TOKEN" \
  --project-key "<project>" \
  --environment-key "<env>" \
  --build-id "$BUILD_ID" \
  [--include-tags @smoke] [--runner-count 4] \
  [--wait-for-results --fail-on-failure]
```

## Steps

1. Confirm the project key and environment key with the user (or list them via `testery list-environments`).
2. Pick a build ID (timestamp or git short SHA).
3. Zip with the excludes above, upload, then `create-test-run` with `--build-id`.
4. For the committed/remote version instead, use `testery-playwright-bdd-run-on-testery-remote`.
